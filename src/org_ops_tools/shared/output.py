"""Output formatter for org-ops-tools.

All tool output goes through this module to ensure consistent
stdout/stderr and format conventions.
"""

from __future__ import annotations

import json
import sys
from typing import Any


def print_output(data: Any, fmt: str = "json") -> None:
    """Print data to stdout in the requested format."""
    if fmt == "json":
        json.dump(data, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    elif fmt == "table":
        _print_table(data)
    else:
        json.dump(data, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")


def print_error(message: str) -> None:
    """Print error to stderr as JSON and exit with code 1."""
    json.dump({"status": "error", "error": message}, sys.stderr)
    sys.stderr.write("\n")
    sys.exit(1)


def print_auth_error() -> None:
    """Print auth error to stderr and exit with code 2."""
    msg = "Authentication required. Run: python -m org_ops_tools.shared.azure_auth --login"
    json.dump({"status": "error", "error": msg}, sys.stderr)
    sys.stderr.write("\n")
    sys.exit(2)


def _print_table(data: Any) -> None:
    """Print data as a formatted table to stdout."""
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        headers = list(data[0].keys())
        # Calculate column widths
        col_widths = {h: len(str(h)) for h in headers}
        for row in data:
            for h in headers:
                val = str(row.get(h, ""))
                col_widths[h] = max(col_widths[h], len(val))

        # Print header
        header_line = "  ".join(f"{h!s:<{col_widths[h]}}" for h in headers)
        sys.stdout.write(header_line + "\n")
        separator = "  ".join("-" * col_widths[h] for h in headers)
        sys.stdout.write(separator + "\n")

        # Print rows
        for row in data:
            row_line = "  ".join(f"{row.get(h, '')!s:<{col_widths[h]}}" for h in headers)
            sys.stdout.write(row_line + "\n")
    elif isinstance(data, dict):
        for key, value in data.items():
            sys.stdout.write(f"{key}: {value}\n")
    else:
        sys.stdout.write(str(data) + "\n")
