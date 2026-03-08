"""Mock Azure authentication CLI for org-ops-tools.

Provides --login, --status, and --clear-cache commands.
All implementations are mocks that return success without
contacting Azure. Real auth will be added later.
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime

from org_ops_tools.shared.output import print_output


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for azure_auth CLI."""
    parser = argparse.ArgumentParser(
        prog="python -m org_ops_tools.shared.azure_auth",
        description="Azure authentication management (mock)",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--login", action="store_true", help="Authenticate with Azure (mock)")
    group.add_argument("--status", action="store_true", help="Show current authentication status")
    group.add_argument("--clear-cache", action="store_true", help="Clear cached credentials")
    return parser


def main() -> None:
    """Entry point for azure_auth CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if args.login:
        _handle_login()
    elif args.status:
        _handle_status()
    elif args.clear_cache:
        _handle_clear_cache()
    else:
        parser.print_help()
        sys.exit(0)


def _handle_login() -> None:
    """Mock login -- always succeeds."""
    print("Mock login successful. Authenticated as mock-user@contoso.com")


def _handle_status() -> None:
    """Mock status -- returns fake token info."""
    token_info = {
        "status": "authenticated",
        "user": "mock-user@contoso.com",
        "tenant_id": "00000000-0000-0000-0000-000000000000",
        "token": "mock-token-xxxxxxxxxxxx",
        "expires_at": datetime.now(UTC).isoformat(),
    }
    print_output(token_info, fmt="json")


def _handle_clear_cache() -> None:
    """Mock clear cache -- always succeeds."""
    print("Token cache cleared successfully.")


if __name__ == "__main__":
    main()
