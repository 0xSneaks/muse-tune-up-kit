"""Tests for the step-14 statement-analyzer MOCK.

Run from upgrade/build:  python3 -m unittest statement_analyzer.test_analyzer
These tests are deliberately NOT part of the build/tests suite: the
analyzer is an unapproved mock, kept out of the shipped suite counts
until the owner approves it (step 14 gate).
"""
import pathlib
import unittest

from memory_os.ledger import validate_fact
from statement_analyzer.analyzer import StatementAnalyzerError, parse_statement

FIXTURE = (pathlib.Path(__file__).parent / "fixtures" / "synthetic_statement.csv").read_text()


class Mock(unittest.TestCase):
    def test_fixture_parses_to_claims_plus_balance(self):
        claims = parse_statement(FIXTURE)
        self.assertEqual(len(claims), 7)  # 6 transactions + 1 closing balance
        self.assertEqual(claims[-1]["predicate"], "other:statement-balance")
        self.assertEqual(claims[-1]["value"]["balance_cents"], 332592)

    def test_every_claim_is_a_valid_ledger_record(self):
        for claim in parse_statement(FIXTURE):
            self.assertEqual(validate_fact(claim), [], claim["id"])

    def test_amounts_reconcile_opening_to_closing(self):
        claims = parse_statement(FIXTURE)
        txns = [c for c in claims if c["predicate"] == "other:statement-transaction"]
        self.assertEqual(100000 + sum(c["value"]["amount_cents"] for c in txns), 332592)

    def test_ids_are_deterministic(self):
        self.assertEqual([c["id"] for c in parse_statement(FIXTURE)],
                         [c["id"] for c in parse_statement(FIXTURE)])

    def test_unmarked_input_is_refused(self):
        real_looking = "date,description,amount_cents,balance_cents\n2026-10-02,X,1,1\n"
        with self.assertRaises(StatementAnalyzerError):
            parse_statement(real_looking)

    def test_non_reconciling_fixture_is_refused(self):
        broken = FIXTURE.replace("334766", "334765")
        with self.assertRaises(StatementAnalyzerError):
            parse_statement(broken)


if __name__ == "__main__":
    unittest.main()
