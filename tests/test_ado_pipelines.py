"""Tests for ADO Pipelines mock CLI tool."""

import json
import subprocess
import sys


def run_pipelines(*args: str) -> subprocess.CompletedProcess[str]:
    """Run python -m org_ops_tools.ado_pipelines with given args."""
    cmd = [sys.executable, "-m", "org_ops_tools.ado_pipelines", *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_pipelines_help():
    result = run_pipelines("--help")
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_pipelines_runs_json():
    result = run_pipelines("runs")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 8
    first = data[0]
    for field in ("id", "pipeline_name", "status", "start_time", "end_time"):
        assert field in first, f"Missing field: {field}"


def test_pipelines_runs_status_filter():
    result = run_pipelines("runs", "--status", "failed")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 1
    for run in data:
        assert run["status"] == "failed"


def test_pipelines_runs_last_limit():
    result = run_pipelines("runs", "--last", "5")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) <= 5


def test_pipelines_logs_json():
    result = run_pipelines("logs")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 5
    first = data[0]
    for field in ("timestamp", "level", "message"):
        assert field in first, f"Missing field: {field}"


def test_pipelines_summary_json():
    result = run_pipelines("summary")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, dict)
    for field in ("total", "succeeded", "failed", "running", "success_rate"):
        assert field in data, f"Missing field: {field}"


def test_pipelines_error_exit_code():
    result = run_pipelines("badcmd")
    assert result.returncode != 0


def test_pipelines_table_format():
    result = run_pipelines("runs", "--format", "table")
    assert result.returncode == 0
    try:
        json.loads(result.stdout)
        raise AssertionError("Table output should not be valid JSON")
    except json.JSONDecodeError:
        pass
    assert "pipeline_name" in result.stdout or "status" in result.stdout
