"""Tests for ADO Repos mock CLI tool."""

import json
import subprocess
import sys


def run_repos(*args: str) -> subprocess.CompletedProcess[str]:
    """Run python -m org_ops_tools.ado_repos with given args."""
    cmd = [sys.executable, "-m", "org_ops_tools.ado_repos", *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_repos_help():
    result = run_repos("--help")
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()


def test_repos_scan_json():
    result = run_repos("scan")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 5
    first = data[0]
    for field in ("name", "default_branch", "last_commit_date", "size_mb"):
        assert field in first, f"Missing field: {field}"


def test_repos_prs_json():
    result = run_repos("prs")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 3
    first = data[0]
    for field in ("id", "title", "author", "status", "created_date"):
        assert field in first, f"Missing field: {field}"


def test_repos_prs_status_filter():
    result = run_repos("prs", "--status", "active")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 1
    for pr in data:
        assert pr["status"] == "active"


def test_repos_policies_json():
    result = run_repos("policies")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 3
    first = data[0]
    for field in ("repo", "branch", "policy_name", "is_compliant", "details"):
        assert field in first, f"Missing field: {field}"


def test_repos_error_exit_code():
    result = run_repos("badcmd")
    assert result.returncode != 0


def test_repos_table_format():
    result = run_repos("scan", "--format", "table")
    assert result.returncode == 0
    try:
        json.loads(result.stdout)
        raise AssertionError("Table output should not be valid JSON")
    except json.JSONDecodeError:
        pass
    assert "name" in result.stdout or "default_branch" in result.stdout
