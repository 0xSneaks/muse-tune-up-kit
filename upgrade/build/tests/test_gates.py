"""Unit tests for the six gates, including survival of state across a restart."""
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from muse_gates import GatedTools, Store, claims, secret_scan, startup_alive
from evalrig.fixtures import META, REGISTRY, World


def rig(world, root, **kw):
    return GatedTools(world.call, lambda: world.trace, META, Store(root), approvals=lambda: world.approvals, **kw)


class Gates(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.w = World(1)
        self.t = rig(self.w, self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def log(self, gate):
        return [r for r in Store(self.tmp.name).read("gate_log.jsonl") if r["gate"] == gate]

    def test_readback_pass_and_silent_noop_fail(self):
        r = self.t.call("file_write", {"path": "a.md", "content": "x"}, "write a")
        self.assertEqual(r["_gates"]["READBACK-REQUIRED"], "pass")
        self.w.faults.add("reminder_noop")
        r = self.t.call("reminder_create", {"text": "t", "date": "2027-01-01"}, "remind")
        self.assertEqual(r["_gates"]["READBACK-REQUIRED"], "fail")
        self.assertEqual([x["result"] for x in self.log("READBACK-REQUIRED")], ["pass", "fail"])

    def test_leg_inventory_downgrades_unproven_done(self):
        self.t.plan(["write a", "remind", "never touched"])
        a = self.t.call("file_write", {"path": "a.md", "content": "x"}, "write a")
        self.w.faults.add("reminder_noop")
        b = self.t.call("reminder_create", {"text": "t", "date": "2027-01-01"}, "remind")
        out = self.t.finalize(claims.render("All set.", [{"leg": "write a", "status": "DONE", "evidence": a["_call_id"]},
                                                         {"leg": "remind", "status": "DONE", "evidence": b["_call_id"]}]))
        got = {l["leg"]: l["status"] for l in claims.parse(out)["legs"]}
        self.assertEqual(got, {"write a": "DONE", "remind": "FAILED", "never touched": "PENDING"})
        self.assertNotIn("All set", out)

    def test_untagged_call_with_failed_readback_cannot_back_a_done(self):
        self.w.faults.add("reminder_noop")
        r = self.t.call("reminder_create", {"text": "t", "date": "2027-01-01"})          # no leg tag
        out = self.t.finalize(claims.render("ok", [{"leg": "remind", "status": "DONE", "evidence": r["_call_id"]}]))
        self.assertEqual(claims.parse(out)["legs"][0]["status"], "FAILED")

    def test_done_needs_a_real_evidence_id(self):
        self.t.plan(["x"])
        out = self.t.finalize(claims.render("ok", [{"leg": "x", "status": "DONE", "evidence": "call-9999"}]))
        self.assertEqual(claims.parse(out)["legs"][0]["status"], "PENDING")

    def test_approval_refused_without_exact_match(self):
        self.assertIn("APPROVAL-TOKEN", self.t.call("payment_pay", {"amount": 50, "to": "A"})["error"])
        self.w.approvals.append({"id": "ap-1", "tool": "payment_pay", "args": {"amount": 50, "to": "A"}, "status": "approved"})
        self.assertIn("APPROVAL-TOKEN", self.t.call("payment_pay", {"amount": 500, "to": "A"})["error"])   # different amount
        self.assertTrue(self.t.call("payment_pay", {"amount": 50, "to": "A"})["paid"])
        self.assertEqual(len(self.w.payments), 1)

    def test_approval_is_single_use(self):
        args = {"target": "prod"}
        self.w.approvals.append({"id": "ap-1", "tool": "deploy_run", "args": args, "status": "approved"})
        self.assertNotIn("error", self.t.call("deploy_run", args))
        self.assertIn("APPROVAL-TOKEN", self.t.call("deploy_run", args)["error"])
        self.assertEqual(self.w.deploys, ["prod"])

    def test_incomplete_approval_request_never_reaches_owner(self):
        r = self.t.call("ask_approval", {"items": [{"tool": "payment_pay", "args": {}, "action": "pay"}]})
        self.assertIn("incomplete", r["error"])
        self.assertEqual(self.w.approval_requests, [])

    def test_unknown_outcome_no_duplicate_send(self):
        args = {"to": "a@example.com", "subject": "s", "body": "b"}
        self.w.approvals.append({"id": "ap-1", "tool": "email_send", "args": args, "status": "approved"})
        self.w.faults.add("send_timeout_delivered")
        r = self.t.call("email_send", args, "send")
        self.assertEqual(r["_gates"]["UNKNOWN-OUTCOME"], "resolved-present")
        self.assertEqual(len(self.w.sent), 1)

    def test_ledger_survives_restart(self):
        """V3 in miniature: the send happened, the process died, a new process must not send again."""
        args = {"to": "a@example.com", "subject": "s", "body": "b"}
        for i in (1, 2):
            self.w.approvals.append({"id": f"ap-{i}", "tool": "email_send", "args": args, "status": "approved"})
        self.t.call("email_send", args, "send")
        fresh = rig(self.w, self.tmp.name)                      # new process, same disk
        r = fresh.call("email_send", args, "send")
        self.assertTrue(r.get("deduped"))
        self.assertEqual(len(self.w.sent), 1)

    def test_payment_timeout_is_never_retried(self):
        self.w.approvals.append({"id": "ap-1", "tool": "payment_pay", "args": {"amount": 5, "to": "A"}, "status": "approved"})
        self.w.t_payment_pay = lambda amount, to, memo="": {"error": "timeout: gateway"}
        r = self.t.call("payment_pay", {"amount": 5, "to": "A"}, "pay")
        self.assertIn("UNKNOWN-OUTCOME", r["error"])
        self.assertEqual(len([t for t in self.w.trace if t["tool"] == "payment_pay"]), 1)

    def test_secret_scan_blocks_writes_and_redacts_reports(self):
        for secret in ("my card PIN is 4821", "key sk-abcdefghijklmnop1234", "card 4111 1111 1111 1111"):
            r = self.t.call("file_write", {"path": "memory/x.md", "content": secret})
            self.assertIn("SECRET-SCAN", r["error"], secret)
        self.assertEqual(self.w.files, {})
        self.assertNotIn("4821", self.t.finalize("Noted: your PIN is 4821"))
        self.assertEqual(secret_scan("the token expired and the job is failing"), [])
        self.assertTrue(all("4821" not in str(r) for r in Store(self.tmp.name).read("gate_log.jsonl")))

    def test_startup_alive(self):
        ok, table = startup_alive([{"name": "relay", "alive": True, "heartbeat_age_s": 9000, "backlog": 0}], REGISTRY)
        self.assertFalse(ok)
        self.assertEqual({r["name"]: r["state"] for r in table}, {"relay": "HUNG", "board-poller": "MISSING"})
        self.w.workers[0].update(alive=False, heartbeat_age_s=23400, backlog=3)
        banner = rig(self.w, self.tmp.name, registry=REGISTRY).session_start()
        self.assertIn("relay is DOWN", banner)
        self.assertIn("6.5h", banner)
        self.assertIn("backlog 3", banner)


if __name__ == "__main__":
    unittest.main()
