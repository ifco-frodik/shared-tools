"""Azure DevOps Repos tool (mock).

Returns realistic hardcoded data for repo scanning, PRs, and branch policies.
"""

from __future__ import annotations

import argparse
import sys

from org_ops_tools.shared.output import print_error, print_output

MOCK_REPOS = [
    {
        "name": "backend-api",
        "default_branch": "main",
        "last_commit_date": "2026-03-06T14:30:00Z",
        "size_mb": 124.5,
        "language": "C#",
    },
    {
        "name": "frontend-app",
        "default_branch": "main",
        "last_commit_date": "2026-03-06T13:15:00Z",
        "size_mb": 89.2,
        "language": "TypeScript",
    },
    {
        "name": "infra-config",
        "default_branch": "main",
        "last_commit_date": "2026-03-05T16:45:00Z",
        "size_mb": 12.8,
        "language": "HCL",
    },
    {
        "name": "shared-libs",
        "default_branch": "main",
        "last_commit_date": "2026-03-04T10:20:00Z",
        "size_mb": 45.3,
        "language": "C#",
    },
    {
        "name": "docs-site",
        "default_branch": "main",
        "last_commit_date": "2026-03-03T09:00:00Z",
        "size_mb": 8.1,
        "language": "Markdown",
    },
    {
        "name": "data-pipelines",
        "default_branch": "develop",
        "last_commit_date": "2026-03-06T11:00:00Z",
        "size_mb": 67.4,
        "language": "Python",
    },
]

MOCK_PRS = [
    {
        "id": 501,
        "title": "Add retry logic for database connections",
        "author": "dev-alice",
        "status": "active",
        "source_branch": "feature/db-retry",
        "target_branch": "main",
        "created_date": "2026-03-06T10:00:00Z",
    },
    {
        "id": 500,
        "title": "Update Terraform provider versions",
        "author": "dev-bob",
        "status": "active",
        "source_branch": "chore/tf-upgrade",
        "target_branch": "main",
        "created_date": "2026-03-05T15:30:00Z",
    },
    {
        "id": 499,
        "title": "Fix auth token refresh race condition",
        "author": "dev-charlie",
        "status": "completed",
        "source_branch": "fix/token-refresh",
        "target_branch": "main",
        "created_date": "2026-03-04T09:00:00Z",
    },
    {
        "id": 498,
        "title": "Add new monitoring dashboard components",
        "author": "dev-alice",
        "status": "completed",
        "source_branch": "feature/monitoring-ui",
        "target_branch": "main",
        "created_date": "2026-03-03T14:00:00Z",
    },
    {
        "id": 497,
        "title": "Deprecated: old logging framework migration",
        "author": "dev-dave",
        "status": "abandoned",
        "source_branch": "chore/logging-migration",
        "target_branch": "main",
        "created_date": "2026-03-01T11:00:00Z",
    },
]

MOCK_POLICIES = [
    {
        "repo": "backend-api",
        "branch": "main",
        "policy_name": "Minimum reviewers",
        "is_compliant": True,
        "details": "Requires 2 reviewers; currently enforced",
    },
    {
        "repo": "backend-api",
        "branch": "main",
        "policy_name": "Build validation",
        "is_compliant": True,
        "details": "CI build must pass before merge",
    },
    {
        "repo": "frontend-app",
        "branch": "main",
        "policy_name": "Minimum reviewers",
        "is_compliant": True,
        "details": "Requires 2 reviewers; currently enforced",
    },
    {
        "repo": "infra-config",
        "branch": "main",
        "policy_name": "Minimum reviewers",
        "is_compliant": False,
        "details": "Requires 2 reviewers; currently set to 0",
    },
    {
        "repo": "shared-libs",
        "branch": "main",
        "policy_name": "Build validation",
        "is_compliant": False,
        "details": "No build validation pipeline configured",
    },
    {
        "repo": "docs-site",
        "branch": "main",
        "policy_name": "Minimum reviewers",
        "is_compliant": True,
        "details": "Requires 1 reviewer; currently enforced",
    },
]


def _add_format_arg(parser: argparse.ArgumentParser) -> None:
    """Add --format argument to a parser."""
    parser.add_argument(
        "--format",
        choices=["json", "table"],
        default="json",
        dest="fmt",
        help="Output format (default: json)",
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser for the ADO Repos tool."""
    parser = argparse.ArgumentParser(
        prog="python -m org_ops_tools.ado_repos",
        description="Query Azure DevOps Repositories (mock)",
    )

    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="Scan repositories")
    _add_format_arg(scan_parser)

    prs_parser = subparsers.add_parser("prs", help="List pull requests")
    prs_parser.add_argument(
        "--status",
        choices=["active", "completed", "abandoned", "all"],
        default="all",
        help="Filter by status (default: all)",
    )
    _add_format_arg(prs_parser)

    policies_parser = subparsers.add_parser("policies", help="Check branch policies")
    _add_format_arg(policies_parser)

    return parser


def main() -> None:
    """Entry point for the ADO Repos mock tool."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command is None:
            parser.print_help()
            sys.exit(0)
        elif args.command == "scan":
            print_output(MOCK_REPOS, fmt=args.fmt)
        elif args.command == "prs":
            data = list(MOCK_PRS)
            if args.status != "all":
                data = [pr for pr in data if pr["status"] == args.status]
            print_output(data, fmt=args.fmt)
        elif args.command == "policies":
            print_output(MOCK_POLICIES, fmt=args.fmt)
        else:
            print_error(f"Unknown command: {args.command}")
    except SystemExit:
        raise
    except Exception as e:
        print_error(str(e))
