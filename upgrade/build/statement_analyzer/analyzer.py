"""Statement analyzer -- STEP 14 PREP, MOCK ONLY.

This module processes NO real statements. It parses exactly one input:
the synthetic fixture format in `fixtures/` of this package, whose
first line must carry the marker "SYNTHETIC FIXTURE"; any other input
is refused (StatementAnalyzerError). All names, amounts and the bank
itself in the fixture are fictional.

ACTIVATION GATE: real statement formats and real data are out of scope
until the owner approves this mock (upgrade step 14). Nothing in the
live system imports this package, and it must stay that way until that
approval exists.

Output: ledger claim records in the memory_os ledger's shape
(spec 02 section 2.1 base fields), one per transaction plus one for
the closing balance, using the ledger's `other:` predicate escape
hatch -- `other:statement-transaction` / `other:statement-balance` --
so every emitted record passes `memory_os.ledger.validate_fact`.
Amounts are integer cents; ids are deterministic digests of the row.
"""
import csv
import hashlib
import io

SYNTHETIC_MARKER = "SYNTHETIC FIXTURE"
SOURCE = "statement-analyzer-mock (synthetic fixture only)"


class StatementAnalyzerError(Exception):
    pass


def _claim_id(kind, *parts):
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return f"stmt-{kind}-{h[:12]}"


def parse_statement(text, account="EXAMPLE-0000", period_end="2026-10-31"):
    """Parse a synthetic statement fixture into ledger claim records.

    Refuses any text whose first line lacks the SYNTHETIC FIXTURE
    marker -- the mechanical half of the mock-only rule in the header.
    Also verifies the running balances reconcile row by row; a fixture
    that does not reconcile is a parse error, not a claim.
    """
    lines = text.lstrip().splitlines()
    if not lines or SYNTHETIC_MARKER not in lines[0]:
        raise StatementAnalyzerError(
            "refused: input is not a marked synthetic fixture; this mock "
            "processes no real statements (see module header)")
    rows = [ln for ln in lines if ln.strip() and not ln.lstrip().startswith("#")]
    reader = csv.DictReader(io.StringIO("\n".join(rows)))
    claims = []
    prev_balance = None
    for row in reader:
        amount = int(row["amount_cents"])
        balance = int(row["balance_cents"])
        if prev_balance is not None and prev_balance + amount != balance:
            raise StatementAnalyzerError(
                f"fixture does not reconcile at {row['date']}: "
                f"{prev_balance} + {amount} != {balance}")
        prev_balance = balance
        claims.append({
            "id": _claim_id("txn", account, row["date"], row["description"], amount),
            "subject": f"account:{account}",
            "predicate": "other:statement-transaction",
            "value": {"date": row["date"], "description": row["description"],
                      "amount_cents": amount, "balance_cents": balance},
            "status": "active",
            "confidence": "tool-observed",
            "source": SOURCE,
            "learned_at": period_end,
        })
    if prev_balance is None:
        raise StatementAnalyzerError("fixture contained no transactions")
    claims.append({
        "id": _claim_id("bal", account, period_end, prev_balance),
        "subject": f"account:{account}",
        "predicate": "other:statement-balance",
        "value": {"as_of": period_end, "balance_cents": prev_balance},
        "status": "active",
        "confidence": "tool-observed",
        "source": SOURCE,
        "learned_at": period_end,
    })
    return claims
