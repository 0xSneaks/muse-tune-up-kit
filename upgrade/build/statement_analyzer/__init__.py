"""Statement analyzer -- MOCK ONLY. See analyzer.py header.

Processes NO real statements. Parses only the synthetic fixture format
in this package, and refuses anything else. Activates (real statement
formats, real data) only on owner approval of the mock -- step 14's
gate. Nothing in the live system imports this package.
"""
from .analyzer import StatementAnalyzerError, parse_statement

__all__ = ["StatementAnalyzerError", "parse_statement"]
