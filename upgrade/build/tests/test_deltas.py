"""Tests for the step-1 deltas: D29 (secret-scan false positives), D7 (labels),
D9 (MASKED-VALUE outcomes) and D10 (standing grants, delegated approvals, gate types)."""
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from muse_gates import GatedTools, Store, claims, secret_scan, masked_value, fingerprint, GATE_TYPES
from muse_gates.store import h
from evalrig.fixtures import META, World

TWELVE = "apple river stone candle orbit velvet maple hollow ribbon cactus lantern copper"
KEY = b"test-only-fingerprint-key"


def kinds(text):
    return {hit if isinstance(hit, str) else hit[0] for hit in secret_scan(text)}


class SecretScanFalsePositives(unittest.TestCase):              # D29
    def test_long_numeric_ids_are_not_cards(self):
        for text in ("message id 1234567890123456789", "user 4532015112830366 joined",
                     "order 4111111111111111 shipped", "chat -1001234567890123 muted",
                     "tx block 18446744073709551615", "snowflake 1098765432109876543 posted"):
            self.assertEqual(secret_scan(text), [], text)

    def test_real_card_context_still_caught(self):
        for text in ("card 4111 1111 1111 1111", "visa 4532-0151-1283-0366 exp 09/29"):
            self.assertNotEqual(secret_scan(text), [], text)

    def test_prose_about_seed_phrases_is_not_a_seed(self):
        for text in ("Never share your seed phrase with anyone, and never type it into a website you do not trust.",
                     "The wallet asks for a twelve word recovery phrase; write it on paper and keep it offline.",
                     "If someone asks for your seed phrase they are trying to steal your funds."):
            self.assertEqual(secret_scan(text), [], text)

    def test_a_bare_seed_is_still_caught(self):
        self.assertNotEqual(secret_scan(TWELVE), [])
        self.assertNotEqual(secret_scan("seed phrase: " + TWELVE), [])
        self.assertEqual(secret_scan(TWELVE + " extra"), [])          # 13 words is not a seed length


class Labels(unittest.TestCase):                                  # D7
    def test_public_label_set_and_aliases(self):
        self.assertEqual(claims.LABELS, ("VERIFIED", "INTENT", "INFERENCE", "UNKNOWN"))
        for raw, want in (("verified", "VERIFIED"), ("INTENT", "INTENT"), ("ASSUMPTION", "INFERENCE"),
                          ("UNVERIFIED", "UNKNOWN"), ("unconfirmed", "UNKNOWN"), ("MAYBE", None), (None, None)):
            self.assertEqual(claims.normalize_label(raw), want, raw)


class MaskedValue(unittest.TestCase):                             # D9
    fp = fingerprint("s3cret-value", KEY)

    def test_absent_is_blocked(self):
        self.assertEqual(masked_value(None, self.fp, KEY)[0], "blocked")
        self.assertEqual(masked_value("", self.fp, KEY)[0], "blocked")

    def test_non_masked_channel(self):
        self.assertEqual(masked_value("s3cret-value", self.fp, KEY)[0], "value-verified")
        self.assertEqual(masked_value("other-value", self.fp, KEY)[0], "blocked")
        self.assertEqual(masked_value("s3cret-value", None, KEY)[0], "presence-verified/value-unverified")

    def test_masked_read_alone_proves_presence_only(self):
        for shown in ("sk-****abcd", "••••", "[REDACTED]", "ab…yz", "xxxxxxxx", "000000"):
            self.assertEqual(masked_value(shown, self.fp, KEY)[0], "presence-verified/value-unverified", shown)

    def test_probe(self):
        good, bad = {"safe": True, "fp": self.fp}, {"safe": True, "fp": fingerprint("nope", KEY)}
        self.assertEqual(masked_value("****", self.fp, KEY, good)[0], "value-verified")
        self.assertEqual(masked_value("****", self.fp, KEY, bad)[0], "blocked")
        for barred in ({"safe": None, "fp": self.fp}, {"safe": False, "fp": self.fp}):
            self.assertEqual(masked_value("****", self.fp, KEY, barred)[0], "presence-verified/value-unverified")

    def test_ordinary_text_is_not_masked(self):
        from muse_gates.gates import is_masked
        for text in ("# Heading\n\n========", "box of 4 xbox games", "taxxing", "see 1.2.3", "a---b"):
            self.assertFalse(is_masked(text), text)


class GateRig(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.w = World(1)

    def tearDown(self):
        self.tmp.cleanup()

    def rig(self, meta=META, **kw):
        return GatedTools(self.w.call, lambda: self.w.trace, meta, Store(self.tmp.name),
                          approvals=lambda: self.w.approvals, **kw)

    def log(self, gate):
        return [r for r in Store(self.tmp.name).read("gate_log.jsonl") if r["gate"] == gate]


class MaskedValueInTheRig(GateRig):                               # D9
    def test_presence_only_leg_cannot_be_done(self):
        t = self.rig()
        t.plan(["rotate key"])
        r = t.call("file_write", {"path": "a.md", "content": "x"}, "rotate key")
        t.verify_value("rotate key", "sk-****abcd", fingerprint("s3cret", KEY), KEY, evidence=r["_call_id"])
        out = t.finalize(claims.render("ok", [{"leg": "rotate key", "status": "DONE", "evidence": r["_call_id"]}]))
        self.assertEqual(claims.parse(out)["legs"][0]["status"], "PENDING")
        self.assertIn("presence-verified / value-unverified", self.log("LEG-INVENTORY")[-1]["detail"])

    def test_blocked_leg_and_verified_leg(self):
        t = self.rig()
        t.plan(["a", "b"])
        ra = t.call("file_write", {"path": "a.md", "content": "x"}, "a")
        rb = t.call("file_write", {"path": "b.md", "content": "y"}, "b")
        fp = fingerprint("s3cret", KEY)
        self.assertEqual(t.verify_value("a", "wrong", fp, KEY), "blocked")
        self.assertEqual(t.verify_value("b", "****", fp, KEY, {"safe": True, "fp": fp}, evidence=rb["_call_id"]),
                         "value-verified")
        out = t.finalize(claims.render("ok", [{"leg": "a", "status": "DONE", "evidence": ra["_call_id"]},
                                              {"leg": "b", "status": "DONE", "evidence": rb["_call_id"]}]))
        self.assertEqual({l["leg"]: l["status"] for l in claims.parse(out)["legs"]}, {"a": "BLOCKED", "b": "DONE"})
        self.assertTrue(all("s3cret" not in str(r) for r in Store(self.tmp.name).read("gate_log.jsonl")))

    def test_masked_value_never_used_as_an_argument(self):
        t = self.rig()
        r = t.call("file_write", {"path": "env.md", "content": "sk-****abcd"}, "copy key")
        self.assertIn("MASKED-VALUE", r["error"])
        self.assertEqual(self.w.files, {})
        self.assertEqual(self.log("MASKED-VALUE")[0]["result"], "blocked")


class ApprovalKinds(GateRig):                                     # D10
    def test_seven_gate_types(self):
        self.assertEqual(len(GATE_TYPES), 7)
        self.assertTrue({m["gated"] for m in META.values() if m.get("gated")} <= set(GATE_TYPES))

    def test_unknown_gate_type_fails_closed(self):
        meta = {**META, "deploy_run": {**META["deploy_run"], "gated": "launch"}}
        t = self.rig(meta)
        self.w.approvals.append({"id": "ap-1", "tool": "deploy_run", "args": {"target": "staging"}, "status": "approved"})
        self.assertIn("unknown gate type", t.call("deploy_run", {"target": "staging"})["error"])
        self.assertEqual(self.w.deploys, [])

    def test_standing_grant_is_reused_and_scoped(self):
        t = self.rig()
        self.w.approvals.append({"id": "sg-1", "kind": "standing_grant", "gate": "deploy", "status": "approved",
                                 "scope": {"tool": "deploy_run", "args": {"target": "preview-*"}}})
        for n in range(3):
            self.assertEqual(t.call("deploy_run", {"target": f"preview-{n}"})["deployed"], f"preview-{n}")
        self.assertIn("APPROVAL-TOKEN", t.call("deploy_run", {"target": "production"})["error"])
        self.assertEqual(self.w.deploys, ["preview-0", "preview-1", "preview-2"])
        self.assertEqual(Store(self.tmp.name).read("approvals_used.jsonl"), [])

    def test_standing_grant_never_covers_money_or_credentials(self):
        t = self.rig()
        self.w.approvals += [
            {"id": "sg-pay", "kind": "standing_grant", "gate": "spend", "status": "approved",
             "scope": {"tool": "payment_pay", "args": {}}},
            {"id": "sg-cred", "kind": "standing_grant", "gate": "credential", "status": "approved",
             "scope": {"tool": "*", "args": {}}}]
        self.assertIn("APPROVAL-TOKEN", t.call("payment_pay", {"amount": 5, "to": "A"})["error"])
        self.assertIn("APPROVAL-TOKEN", t.call("credential_update", {"service": "mail"})["error"])
        self.assertEqual((self.w.payments, self.w.cred_updates), ([], []))

    def test_standing_grant_for_another_gate_does_not_apply(self):
        t = self.rig()
        self.w.approvals.append({"id": "sg-1", "kind": "standing_grant", "gate": "delete", "status": "approved",
                                 "scope": {"tool": "*", "args": {}}})
        self.assertIn("APPROVAL-TOKEN", t.call("deploy_run", {"target": "preview-1"})["error"])

    def test_delegated_approval(self):
        call = ("deploy_run", {"target": "staging"})
        rec = {"id": "da-1", "kind": "delegated_approval", "gate": "deploy", "tool": "deploy_run",
               "reviewer": "reviewer-a", "packet_hash": h(list(call)), "status": "approved"}
        # reviewer the owner never named: ignored
        self.w.approvals.append({**rec, "id": "da-0", "reviewer": "stranger"})
        t = self.rig(delegates=["reviewer-a"])
        self.assertIn("APPROVAL-TOKEN", t.call(*call)["error"])
        # named reviewer, different packet: ignored
        self.w.approvals.append({**rec, "id": "da-2", "packet_hash": h(["deploy_run", {"target": "production"}])})
        self.assertIn("APPROVAL-TOKEN", t.call(*call)["error"])
        # named reviewer, matching packet: allowed once
        self.w.approvals.append(rec)
        self.assertEqual(t.call(*call)["deployed"], "staging")
        self.assertIn("APPROVAL-TOKEN", t.call(*call)["error"])
        self.assertEqual(self.w.deploys, ["staging"])
        self.assertEqual([r["detail"] for r in self.log("APPROVAL-TOKEN") if r["result"] == "pass"],
                         ["delegated_approval"])


if __name__ == "__main__":
    unittest.main()
