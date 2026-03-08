"""Tests for SQLMI mock CLI tool."""

import json
import subprocess
import sys


def run_sqlmi(*args: str) -> subprocess.CompletedProcess[str]:
    """Run python -m org_ops_tools.sqlmi with given args."""
    cmd = [sys.executable, "-m", "org_ops_tools.sqlmi", *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_sqlmi_help():
    result = run_sqlmi("--help")
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_sqlmi_critical_alerts_json():
    result = run_sqlmi("--preset", "critical-alerts")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 3
    first = data[0]
    for field in ("alert_id", "server", "severity", "message", "timestamp", "status"):
        assert field in first, f"Missing field: {field}"


def test_sqlmi_recent_queries_json():
    result = run_sqlmi("--preset", "recent-queries")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 3
    assert "query_id" in data[0]


def test_sqlmi_performance_summary_json():
    result = run_sqlmi("--preset", "performance-summary")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, dict)
    assert "metrics" in data


def test_sqlmi_unknown_preset():
    result = run_sqlmi("--preset", "nonexistent")
    # argparse rejects invalid choices with exit code 2
    assert result.returncode != 0


def test_sqlmi_table_format():
    result = run_sqlmi("--preset", "critical-alerts", "--format", "table")
    assert result.returncode == 0
    # Table output should not be valid JSON
    try:
        json.loads(result.stdout)
        raise AssertionError("Table output should not be valid JSON")
    except json.JSONDecodeError:
        pass
    # Should contain header-like text
    assert "alert_id" in result.stdout or "severity" in result.stdout


def test_sqlmi_no_args_shows_help():
    result = run_sqlmi()
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()
