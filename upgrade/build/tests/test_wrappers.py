"""Unit tests for the step-6 ENFORCED-WRAPPER gates: each gate must fire
(block the bad call, without invoking the wrapped tool) and pass (let the
good call through unchanged), and must log in GatedTools' record shape."""
import json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from muse_gates import Store
from wrappers import InventoryDistinctness, LedgerAppendOnly, ManifestComplete, SecretScanSend


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def log(self, gate):
        return [r for r in self.store.read("gate_log.jsonl") if r["gate"] == gate]


class Ledger(Base):
    def _write_tool(self):
        calls = []

        def raw_write(path, text):
            calls.append((path, text))
            with open(path, "w") as f:
                f.write(text)
            return {"ok": True}

        return raw_write, calls

    def test_append_passes_rewrite_and_truncate_blocked(self):
        path = os.path.join(self.tmp.name, "ledger.jsonl")
        with open(path, "w") as f:
            f.write("line1\n")
        raw, calls = self._write_tool()
        w = LedgerAppendOnly(self.store).wrap(raw)

        r = w(path, "line1\nline2\n")                       # pure append: allowed
        self.assertEqual(r, {"ok": True})
        with open(path) as f:
            self.assertEqual(f.read(), "line1\nline2\n")

        r = w(path, "line1\nEDITED\nline2\n")               # rewrite a past line: blocked
        self.assertIn("LEDGER-APPEND-ONLY", r["error"])
        r = w(path, "line1\n")                              # truncate: blocked
        self.assertIn("LEDGER-APPEND-ONLY", r["error"])
        with open(path) as f:
            self.assertEqual(f.read(), "line1\nline2\n")    # ledger untouched by blocked calls
        self.assertEqual(len(calls), 1)                     # wrapped tool ran only for the append
        self.assertEqual([x["result"] for x in self.log("LEDGER-APPEND-ONLY")],
                         ["pass", "fail", "fail"])

    def test_new_file_passes(self):
        raw, _ = self._write_tool()
        w = LedgerAppendOnly(self.store).wrap(raw)
        path = os.path.join(self.tmp.name, "fresh.jsonl")
        self.assertEqual(w(path, "first\n"), {"ok": True})


class Distinctness(Base):
    def test_shared_backend_collapses_and_blocks(self):
        w = InventoryDistinctness(self.store)
        same = [{"name": "board", "backend": "ai-coms", "operator": "crew", "mechanism": "git"},
                {"name": "board-mirror", "backend": "ai-coms", "operator": "crew", "mechanism": "api"}]
        ok, _ = w.check(same)
        self.assertFalse(ok)                                # two names, one infrastructure

        ran = []
        wrapped = w.wrap(lambda args: ran.append(args) or {"ok": True},
                         lambda args: args["sources"])
        r = wrapped({"sources": same})
        self.assertIn("INVENTORY-DISTINCTNESS", r["error"])
        self.assertEqual(ran, [])                           # tool never invoked

    def test_distinct_sources_pass_and_mechanism_sharing_counts(self):
        w = InventoryDistinctness(self.store)
        distinct = [{"name": "a", "backend": "github", "operator": "x", "mechanism": "git"},
                    {"name": "b", "backend": "local-fs", "operator": "y", "mechanism": "walk"}]
        ok, _ = w.check(distinct)
        self.assertTrue(ok)
        # three declared, two sharing a mechanism -> still 2 distinct classes
        trio = distinct + [{"name": "c", "backend": "other", "operator": "z", "mechanism": "git"}]
        self.assertEqual(InventoryDistinctness.distinct_count(trio), 2)
        ok, _ = w.check(trio, required=2)
        self.assertTrue(ok)
        ok, _ = w.check(trio, required=3)
        self.assertFalse(ok)
        wrapped = w.wrap(lambda args: {"ok": True, "seen": args}, lambda args: args["sources"])
        self.assertEqual(wrapped({"sources": distinct})["ok"], True)
        # check() alone does not log; only wrapped calls do
        self.assertEqual([x["result"] for x in self.log("INVENTORY-DISTINCTNESS")], ["pass"])


class SecretScanSendSide(Base):
    SECRET = "sk-TESTKEY0123456789abcdef"

    def test_secret_payload_blocked_and_value_never_logged(self):
        sent = []
        w = SecretScanSend(self.store).wrap(lambda args: sent.append(args) or {"ok": True})
        r = w({"text": f"deploy with key {self.SECRET}", "channel": "ops"})
        self.assertIn("SECRET-SCAN", r["error"])
        self.assertEqual(sent, [])                          # send never happened
        log_text = json.dumps(self.store.read("gate_log.jsonl"))
        self.assertIn("api-key", log_text)                  # class is logged
        self.assertNotIn(self.SECRET, log_text)             # value is not

    def test_clean_payload_passes_through(self):
        w = SecretScanSend(self.store).wrap(lambda args: {"ok": True, "echo": args})
        args = {"text": "standup notes are ready", "channel": "ops"}
        self.assertEqual(w(args)["echo"], args)
        self.assertEqual([x["result"] for x in self.log("SECRET-SCAN")], ["pass"])


class Manifest(Base):
    LISTING = ["a.md", "b.md", "c.md"]

    def test_complete_manifest_passes(self):
        w = ManifestComplete(self.store)
        man = {"scope": "authored tree only", "files": ["a.md", "b.md"], "excluded": ["c.md"]}
        ok, _ = w.check(man, self.LISTING)
        self.assertTrue(ok)
        wrapped = w.wrap(lambda args: {"ok": True},
                         lambda args: args["manifest"], lambda args: args["listing"])
        self.assertEqual(wrapped({"manifest": man, "listing": self.LISTING}), {"ok": True})

    def test_missing_extra_and_scopeless_all_block(self):
        w = ManifestComplete(self.store)
        ran = []
        wrapped = w.wrap(lambda args: ran.append(args) or {"ok": True},
                         lambda args: args["manifest"], lambda args: args["listing"])
        cases = [
            {"scope": "s", "files": ["a.md", "gone.md"]},                    # listed but absent
            {"scope": "s", "files": ["a.md", "b.md"]},                       # c.md unaccounted
            {"files": ["a.md", "b.md", "c.md"]},                             # no scope line (D8)
        ]
        for man in cases:
            r = wrapped({"manifest": man, "listing": self.LISTING})
            self.assertIn("MANIFEST-COMPLETE", r["error"])
        self.assertEqual(ran, [])
        self.assertEqual([x["result"] for x in self.log("MANIFEST-COMPLETE")],
                         ["fail", "fail", "fail"])


if __name__ == "__main__":
    unittest.main()
