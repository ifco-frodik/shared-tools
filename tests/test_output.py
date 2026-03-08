"""Tests for org_ops_tools.shared.output module."""

import json
import subprocess
import sys

import pytest


class TestPrintOutputJson:
    """Test print_output with JSON format."""

    def test_json_format_produces_valid_json(self, capsys: pytest.CaptureFixture[str]) -> None:
        from org_ops_tools.shared.output import print_output

        data = {"key": "value", "count": 42}
        print_output(data, fmt="json")
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed == {"key": "value", "count": 42}

    def test_json_format_indent_2(self, capsys: pytest.CaptureFixture[str]) -> None:
        from org_ops_tools.shared.output import print_output

        data = {"a": 1}
        print_output(data, fmt="json")
        captured = capsys.readouterr()
        assert '  "a": 1' in captured.out

    def test_json_format_list_of_dicts(self, capsys: pytest.CaptureFixture[str]) -> None:
        from org_ops_tools.shared.output import print_output

        data = [{"name": "one"}, {"name": "two"}]
        print_output(data, fmt="json")
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert len(parsed) == 2

    def test_json_default_format(self, capsys: pytest.CaptureFixture[str]) -> None:
        from org_ops_tools.shared.output import print_output

        data = {"test": True}
        print_output(data)  # default should be json
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["test"] is True


class TestPrintOutputTable:
    """Test print_output with table format."""

    def test_table_format_list_of_dicts(self, capsys: pytest.CaptureFixture[str]) -> None:
        from org_ops_tools.shared.output import print_output

        data = [
            {"name": "alice", "role": "admin"},
            {"name": "bob", "role": "user"},
        ]
        print_output(data, fmt="table")
        captured = capsys.readouterr()
        assert "name" in captured.out
        assert "role" in captured.out
        assert "alice" in captured.out
        assert "bob" in captured.out

    def test_table_format_has_headers(self, capsys: pytest.CaptureFixture[str]) -> None:
        from org_ops_tools.shared.output import print_output

        data = [{"col1": "val1", "col2": "val2"}]
        print_output(data, fmt="table")
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) >= 2  # at least header + one data row


class TestPrintError:
    """Test print_error function."""

    def test_print_error_exits_with_code_1(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", "from org_ops_tools.shared.output import print_error; print_error('test error')"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1

    def test_print_error_writes_json_to_stderr(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", "from org_ops_tools.shared.output import print_error; print_error('bad thing')"],
            capture_output=True,
            text=True,
        )
        error = json.loads(result.stderr)
        assert error["status"] == "error"
        assert error["error"] == "bad thing"

    def test_print_error_nothing_on_stdout(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", "from org_ops_tools.shared.output import print_error; print_error('oops')"],
            capture_output=True,
            text=True,
        )
        assert result.stdout.strip() == ""


class TestPrintAuthError:
    """Test print_auth_error function."""

    def test_print_auth_error_exits_with_code_2(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", "from org_ops_tools.shared.output import print_auth_error; print_auth_error()"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2

    def test_print_auth_error_writes_json_to_stderr(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", "from org_ops_tools.shared.output import print_auth_error; print_auth_error()"],
            capture_output=True,
            text=True,
        )
        error = json.loads(result.stderr)
        assert error["status"] == "error"
        assert "auth" in error["error"].lower() or "login" in error["error"].lower()
