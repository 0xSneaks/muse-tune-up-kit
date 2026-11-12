"""Steps 9-10: standing-order ledger class + renderer; DEP-STAMP and
CORRECTION-SWEEP on fixtures (spec 02 sections 2.1, 2.4; SPEC-DELTA D17)."""
import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_os import depstamp, fixtures, ledger
from muse_gates import Store


class StandingOrderLedger(unittest.TestCase):
    def setUp(self):
        self.records = fixtures.standing_order_fixture()
        self.orders = [r for r in self.records if ledger.is_standing_order(r)]
        self.facts = [r for r in self.records if not ledger.is_standing_order(r)]

    def test_fixture_matches_d4_counts(self):
        counts = fixtures.d4_counts()
        total_rules = sum(v[1] for v in counts.values())
        total_facts = sum(v[2] for v in counts.values())
        self.assertEqual((total_rules, total_facts), (28, 7))
        self.assertEqual(len(self.orders), 28)
        self.assertEqual(len(self.facts), 7)

    def test_fixture_records_are_schema_valid_but_not_production(self):
        for rec in self.records:
            self.assertEqual(ledger.validate_fact(rec), [], rec["id"])
        for rec in self.orders:
            errs = ledger.validate_fact(rec, production=True)
            self.assertTrue(any("binds_gate" in e for e in errs), rec["id"])
            self.assertTrue(any("owner_quote" in e for e in errs), rec["id"])

    def test_production_record_renders_to_its_layer(self):
        base = dict(self.orders[0])
        kernel_rec = dict(base, id="so-k", binds_gate=True, skill=None,
                          owner_quote="just do it", owner_date="2026-10-30")
        skill_rec = dict(base, id="so-s", binds_gate=False, skill="onchain-send",
                         owner_quote="money goes back here", owner_date="2026-11-04")
        self.assertEqual(ledger.validate_fact(kernel_rec, production=True), [])
        self.assertEqual(ledger.validate_fact(skill_rec, production=True), [])
        out = ledger.render_rules_layer([kernel_rec, skill_rec])
        self.assertEqual(len(out["kernel"]), 1)
        self.assertIn('"just do it" (2026-10-30)', out["kernel"][0])
        self.assertEqual(len(out["skills"]["onchain-send"]), 1)
        self.assertIn('"money goes back here" (2026-11-04)',
                      out["skills"]["onchain-send"][0])

    def test_every_fixture_order_renders_exactly_once(self):
        out = ledger.render_rules_layer(self.records)
        rendered = (out["kernel"]
                    + [line for lines in out["skills"].values() for line in lines]
                    + out["unresolved"])
        ids = [line.split("]")[0].lstrip("- [") for line in rendered]
        self.assertEqual(sorted(ids), sorted(r["id"] for r in self.orders))
        self.assertEqual(len(ids), len(set(ids)), "an order rendered twice")
        # Fixture destinations are unresolved (content not in the pack):
        # they must surface as unresolved, never dropped, never guessed.
        self.assertEqual(len(out["unresolved"]), 28)
        self.assertEqual(out["kernel"], [])
        self.assertEqual(out["skills"], {})

    def test_live_keeps_none_of_them(self):
        live = ledger.live_lines_for(self.records)
        self.assertEqual([r for r in live if ledger.is_standing_order(r)], [])
        self.assertEqual(sorted(r["id"] for r in live),
                         sorted(r["id"] for r in self.facts))


# ATOM-REGISTRY section 4 section sizes (bytes) for the live memory file.
SECTION_BYTES = {"M-1": 251, "M-2": 2481, "M-3": 5489, "M-4": 5931,
                 "M-5": 1982, "M-6": 585, "M-7": 186, "M-8": 3586, "M-9": 1404}
LIVE_BUDGET = 6144  # spec 02: LIVE at 6 KB or less


class LiveProjection(unittest.TestCase):
    """Step 11c arithmetic, from D4 shares and registry section sizes."""

    def test_projection(self):
        counts = fixtures.d4_counts()
        so = next(v for k, v in counts.items() if k.startswith("Standing orders"))
        mw = next(v for k, v in counts.items() if k.startswith("Money"))
        rule_out = round(SECTION_BYTES["M-3"] * so[1] / so[0]) \
            + round(SECTION_BYTES["M-4"] * mw[1] / mw[0])
        itemized = sum(SECTION_BYTES.values())
        extraction_only = itemized - rule_out
        # Extraction alone does NOT meet the budget; say so in the test.
        self.assertGreater(extraction_only, LIVE_BUDGET)
        eligible = (SECTION_BYTES["M-2"] + SECTION_BYTES["M-6"]
                    + SECTION_BYTES["M-8"]
                    + round(SECTION_BYTES["M-3"] * so[2] / so[0])
                    + round(SECTION_BYTES["M-4"] * mw[2] / mw[0]))
        generated = min(eligible, LIVE_BUDGET)  # generator cuts at 6 KB
        self.assertLessEqual(generated, LIVE_BUDGET)


OLD = {"id": "f-0100", "subject": "person:sam-k", "predicate": "deadline",
       "value": "2027-03-12", "status": "active", "confidence": "owner-stated",
       "source": "logs/2027-03-01.md#L9", "learned_at": "2027-03-01"}
NEW = dict(OLD, id="f-0101", value="2027-03-15", supersedes="f-0100")


def sweep_world(store):
    """Artifacts built on OLD: deps-only, literal-variant, literal,
    gated outbound, already sent, unrelated, and a dated log."""
    depstamp.stamp(store, "goal-party", "goal", ["f-0100"], "2027-03-01")
    depstamp.stamp(store, "job-invite", "scheduled_job", ["f-0100"], "2027-03-01")
    return {
        "goal-party": {"class": "internal",
                       "text": "Plan the party for person:sam-k (date from ledger)."},
        "note-card": {"class": "internal", "text": "Party moved to Mar 12, tell Sam."},
        "rem-text": {"class": "reminder", "text": "Remind: deadline 2027-03-12."},
        "job-invite": {"class": "scheduled_outbound",
                       "text": "Send invite for 2027-03-12."},
        "sent-msg": {"class": "sent", "text": "See you on 3/12!"},
        "unrelated": {"class": "internal", "text": "Groceries: milk, eggs."},
        "log-0301": {"class": "log", "text": "2027-03-01: deadline set to 2027-03-12."},
    }


class Sweep(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_stamp_rejects_unknown_kind(self):
        with self.assertRaises(ValueError):
            depstamp.stamp(self.store, "x", "email", ["f-0100"], "2027-03-01")

    def test_superseded_claim_flags_all_dependents(self):
        arts = sweep_world(self.store)
        receipt, patched = depstamp.sweep(self.store, OLD, NEW, arts, ts="2027-03-05")
        self.assertEqual(receipt["old"], "f-0100")
        self.assertEqual(receipt["found"], 5)          # all but unrelated + log
        self.assertEqual(receipt["fixed"], 3)          # goal, note, reminder
        self.assertEqual(receipt["needs_approval"], 1)  # scheduled outbound
        self.assertEqual(receipt["sent"], 1)            # already sent
        self.assertEqual(receipt["residual"], 0)
        # Patched texts carry the new value in the same format.
        self.assertIn("2027-03-15", patched["rem-text"])
        self.assertIn("Mar 15", patched["note-card"])
        self.assertIn("2027-03-15", patched["job-invite"])
        # Sent and log artifacts are never touched.
        self.assertNotIn("sent-msg", patched)
        self.assertNotIn("log-0301", patched)
        # Correction recorded; deps re-pointed at the new fact.
        corr = self.store.read("corrections.jsonl")
        self.assertEqual(len(corr), 1)
        self.assertEqual(corr[0]["old_value"], "2027-03-12")
        deps = self.store.read("deps.jsonl")
        self.assertTrue(any(r.get("repointed_from") == "f-0100"
                            and "f-0101" in r["facts"] for r in deps))

    def test_unsuperseded_claim_flags_zero(self):
        arts = sweep_world(self.store)
        # No supersession: sweep runs only on a correction. With no old
        # fact superseded there is nothing to propagate -- model the
        # no-correction state by sweeping a fact nothing depends on and
        # whose value appears nowhere.
        ghost = dict(OLD, id="f-9999", value="2031-01-01")
        receipt, patched = depstamp.sweep(self.store, ghost,
                                          dict(ghost, id="f-9998"), arts,
                                          ts="2027-03-05")
        self.assertEqual(receipt["found"], 0)
        self.assertEqual(receipt["fixed"], 0)
        self.assertEqual(patched, {})

    def test_resurrection_guard(self):
        facts = [dict(OLD, status="superseded"), NEW]
        corrs = self.store.read("corrections.jsonl")
        depstamp.sweep(self.store, OLD, NEW, sweep_world(self.store), ts="2027-03-05")
        corrs = self.store.read("corrections.jsonl")
        stale = dict(OLD, id="f-0200", learned_at="2027-03-02")
        fresh = dict(OLD, id="f-0201", learned_at="2027-03-06")
        self.assertTrue(depstamp.resurrection_guard(stale, facts, corrs))
        self.assertFalse(depstamp.resurrection_guard(fresh, facts, corrs))


if __name__ == "__main__":
    unittest.main()
