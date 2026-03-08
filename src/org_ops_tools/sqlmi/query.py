"""Azure SQL Managed Instance query tool (mock).

Returns realistic hardcoded data for SQLMI monitoring presets.
"""

from __future__ import annotations

import argparse
import sys

from org_ops_tools.shared.output import print_error, print_output

MOCK_CRITICAL_ALERTS = [
    {
        "alert_id": "ALT-001",
        "server": "app-db-01.database.windows.net",
        "database": "prod-orders",
        "severity": "critical",
        "message": "CPU utilization exceeded 95% for 15 minutes",
        "timestamp": "2026-03-06T14:32:00Z",
        "status": "active",
    },
    {
        "alert_id": "ALT-002",
        "server": "app-db-02.database.windows.net",
        "database": "prod-inventory",
        "severity": "warning",
        "message": "Storage usage at 85% capacity",
        "timestamp": "2026-03-06T13:15:00Z",
        "status": "active",
    },
    {
        "alert_id": "ALT-003",
        "server": "analytics-db-01.database.windows.net",
        "database": "reporting",
        "severity": "critical",
        "message": "Deadlock detected on table dbo.transactions",
        "timestamp": "2026-03-06T12:45:00Z",
        "status": "resolved",
    },
    {
        "alert_id": "ALT-004",
        "server": "app-db-01.database.windows.net",
        "database": "prod-orders",
        "severity": "warning",
        "message": "Long-running query detected (> 30 seconds)",
        "timestamp": "2026-03-06T11:20:00Z",
        "status": "active",
    },
]

MOCK_RECENT_QUERIES = [
    {
        "query_id": "QRY-001",
        "database": "prod-orders",
        "query_text": "SELECT TOP 100 * FROM orders WHERE status = 'pending' ORDER BY created_at DESC",
        "duration_ms": 234,
        "rows_returned": 87,
        "executed_at": "2026-03-06T14:30:00Z",
        "status": "completed",
    },
    {
        "query_id": "QRY-002",
        "database": "prod-inventory",
        "query_text": "UPDATE inventory SET quantity = quantity - 1 WHERE sku = 'WIDGET-001'",
        "duration_ms": 12,
        "rows_returned": 0,
        "executed_at": "2026-03-06T14:28:00Z",
        "status": "completed",
    },
    {
        "query_id": "QRY-003",
        "database": "reporting",
        "query_text": "SELECT COUNT(*) FROM daily_aggregates WHERE report_date = '2026-03-05'",
        "duration_ms": 1523,
        "rows_returned": 1,
        "executed_at": "2026-03-06T14:25:00Z",
        "status": "completed",
    },
    {
        "query_id": "QRY-004",
        "database": "prod-orders",
        "query_text": "DELETE FROM temp_cart WHERE expires_at < GETUTCDATE()",
        "duration_ms": 45678,
        "rows_returned": 0,
        "executed_at": "2026-03-06T14:20:00Z",
        "status": "timeout",
    },
]

MOCK_PERFORMANCE_SUMMARY = {
    "server": "app-db-01.database.windows.net",
    "period": "last_24h",
    "metrics": {
        "cpu_percent": 72.5,
        "memory_percent": 64.3,
        "io_percent": 45.8,
        "active_connections": 128,
        "avg_query_duration_ms": 342.7,
    },
    "top_wait_types": [
        {"wait_type": "PAGEIOLATCH_SH", "avg_wait_ms": 12.4},
        {"wait_type": "LCK_M_S", "avg_wait_ms": 8.1},
        {"wait_type": "ASYNC_NETWORK_IO", "avg_wait_ms": 5.6},
    ],
}

PRESETS = {
    "critical-alerts": MOCK_CRITICAL_ALERTS,
    "recent-queries": MOCK_RECENT_QUERIES,
    "performance-summary": MOCK_PERFORMANCE_SUMMARY,
}


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser for the SQLMI tool."""
    parser = argparse.ArgumentParser(
        prog="python -m org_ops_tools.sqlmi",
        description="Query Azure SQL Managed Instance (mock)",
    )
    parser.add_argument(
        "--preset",
        choices=list(PRESETS.keys()),
        help="Use a predefined query preset",
    )
    parser.add_argument(
        "--format",
        choices=["json", "table"],
        default="json",
        dest="fmt",
        help="Output format (default: json)",
    )
    return parser


def main() -> None:
    """Entry point for the SQLMI mock tool."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.preset:
            data = PRESETS[args.preset]
            print_output(data, fmt=args.fmt)
        else:
            parser.print_help()
            sys.exit(0)
    except SystemExit:
        raise
    except Exception as e:
        print_error(str(e))
