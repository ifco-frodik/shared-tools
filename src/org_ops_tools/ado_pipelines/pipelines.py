"""Azure DevOps Pipelines tool (mock).

Returns realistic hardcoded data for pipeline runs, logs, and summary.
"""

from __future__ import annotations

import argparse
import sys

from org_ops_tools.shared.output import print_error, print_output

MOCK_PIPELINE_RUNS = [
    {
        "id": 1042,
        "pipeline_name": "deploy-pipeline",
        "status": "succeeded",
        "start_time": "2026-03-06T14:00:00Z",
        "end_time": "2026-03-06T14:12:30Z",
        "branch": "main",
        "triggered_by": "merge",
    },
    {
        "id": 1041,
        "pipeline_name": "build-api",
        "status": "failed",
        "start_time": "2026-03-06T13:45:00Z",
        "end_time": "2026-03-06T13:52:18Z",
        "branch": "feature/auth-refactor",
        "triggered_by": "push",
    },
    {
        "id": 1040,
        "pipeline_name": "test-suite",
        "status": "succeeded",
        "start_time": "2026-03-06T13:30:00Z",
        "end_time": "2026-03-06T13:38:45Z",
        "branch": "main",
        "triggered_by": "schedule",
    },
    {
        "id": 1039,
        "pipeline_name": "infra-terraform",
        "status": "running",
        "start_time": "2026-03-06T14:10:00Z",
        "end_time": None,
        "branch": "main",
        "triggered_by": "manual",
    },
    {
        "id": 1038,
        "pipeline_name": "release-prod",
        "status": "succeeded",
        "start_time": "2026-03-06T12:00:00Z",
        "end_time": "2026-03-06T12:25:00Z",
        "branch": "release/v2.1.0",
        "triggered_by": "tag",
    },
    {
        "id": 1037,
        "pipeline_name": "build-api",
        "status": "succeeded",
        "start_time": "2026-03-06T11:30:00Z",
        "end_time": "2026-03-06T11:37:22Z",
        "branch": "main",
        "triggered_by": "push",
    },
    {
        "id": 1036,
        "pipeline_name": "deploy-pipeline",
        "status": "failed",
        "start_time": "2026-03-06T10:15:00Z",
        "end_time": "2026-03-06T10:18:05Z",
        "branch": "hotfix/db-timeout",
        "triggered_by": "push",
    },
    {
        "id": 1035,
        "pipeline_name": "test-suite",
        "status": "succeeded",
        "start_time": "2026-03-06T09:00:00Z",
        "end_time": "2026-03-06T09:08:12Z",
        "branch": "main",
        "triggered_by": "schedule",
    },
    {
        "id": 1034,
        "pipeline_name": "security-scan",
        "status": "succeeded",
        "start_time": "2026-03-06T08:00:00Z",
        "end_time": "2026-03-06T08:15:30Z",
        "branch": "main",
        "triggered_by": "schedule",
    },
    {
        "id": 1033,
        "pipeline_name": "build-frontend",
        "status": "running",
        "start_time": "2026-03-06T14:05:00Z",
        "end_time": None,
        "branch": "feature/new-dashboard",
        "triggered_by": "push",
    },
]

MOCK_LOG_ENTRIES = [
    {
        "timestamp": "2026-03-06T13:45:00Z",
        "level": "info",
        "pipeline": "build-api",
        "message": "Build started for feature/auth-refactor",
    },
    {
        "timestamp": "2026-03-06T13:47:30Z",
        "level": "info",
        "pipeline": "build-api",
        "message": "Restoring NuGet packages...",
    },
    {
        "timestamp": "2026-03-06T13:49:15Z",
        "level": "warning",
        "pipeline": "build-api",
        "message": "Package 'Newtonsoft.Json 12.0.3' is deprecated, consider upgrading",
    },
    {
        "timestamp": "2026-03-06T13:51:00Z",
        "level": "error",
        "pipeline": "build-api",
        "message": "Test 'AuthController.Login_InvalidCredentials' failed: expected 401, got 500",
    },
    {
        "timestamp": "2026-03-06T13:52:18Z",
        "level": "error",
        "pipeline": "build-api",
        "message": "Build failed with 1 error(s) and 1 warning(s)",
    },
    {
        "timestamp": "2026-03-06T14:00:00Z",
        "level": "info",
        "pipeline": "deploy-pipeline",
        "message": "Deployment to staging environment started",
    },
]


def _compute_summary() -> dict[str, object]:
    """Compute summary statistics from mock runs data."""
    total = len(MOCK_PIPELINE_RUNS)
    succeeded = sum(1 for r in MOCK_PIPELINE_RUNS if r["status"] == "succeeded")
    failed = sum(1 for r in MOCK_PIPELINE_RUNS if r["status"] == "failed")
    running = sum(1 for r in MOCK_PIPELINE_RUNS if r["status"] == "running")
    success_rate = round((succeeded / total) * 100, 1) if total > 0 else 0.0
    return {
        "total": total,
        "succeeded": succeeded,
        "failed": failed,
        "running": running,
        "success_rate": success_rate,
    }


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
    """Build the argparse parser for the ADO Pipelines tool."""
    parser = argparse.ArgumentParser(
        prog="python -m org_ops_tools.ado_pipelines",
        description="Query Azure DevOps Pipelines (mock)",
    )

    subparsers = parser.add_subparsers(dest="command")

    runs_parser = subparsers.add_parser("runs", help="List pipeline runs")
    runs_parser.add_argument(
        "--status",
        choices=["succeeded", "failed", "running", "all"],
        default="all",
        help="Filter by status (default: all)",
    )
    runs_parser.add_argument(
        "--last",
        type=int,
        default=0,
        help="Limit to last N runs (default: all)",
    )
    _add_format_arg(runs_parser)

    logs_parser = subparsers.add_parser("logs", help="Show recent pipeline log entries")
    _add_format_arg(logs_parser)

    summary_parser = subparsers.add_parser("summary", help="Show pipeline run summary statistics")
    _add_format_arg(summary_parser)

    return parser


def main() -> None:
    """Entry point for the ADO Pipelines mock tool."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command is None:
            parser.print_help()
            sys.exit(0)
        elif args.command == "runs":
            data = list(MOCK_PIPELINE_RUNS)
            if args.status != "all":
                data = [r for r in data if r["status"] == args.status]
            if args.last > 0:
                data = data[: args.last]
            print_output(data, fmt=args.fmt)
        elif args.command == "logs":
            print_output(MOCK_LOG_ENTRIES, fmt=args.fmt)
        elif args.command == "summary":
            print_output(_compute_summary(), fmt=args.fmt)
        else:
            print_error(f"Unknown command: {args.command}")
    except SystemExit:
        raise
    except Exception as e:
        print_error(str(e))
