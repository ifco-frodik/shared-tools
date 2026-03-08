"""Tests for org_ops_tools.shared.azure_auth module."""

import json
import subprocess
import sys


class TestAzureAuthLogin:
    """Test azure_auth --login flag."""

    def test_login_exits_0(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "org_ops_tools.shared.azure_auth", "--login"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_login_prints_success_message(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "org_ops_tools.shared.azure_auth", "--login"],
            capture_output=True,
            text=True,
        )
        assert "successful" in result.stdout.lower()


class TestAzureAuthStatus:
    """Test azure_auth --status flag."""

    def test_status_exits_0(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "org_ops_tools.shared.azure_auth", "--status"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_status_returns_valid_json(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "org_ops_tools.shared.azure_auth", "--status"],
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        assert isinstance(data, dict)

    def test_status_has_token_fields(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "org_ops_tools.shared.azure_auth", "--status"],
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        assert "token" in data or "access_token" in data or "status" in data


class TestAzureAuthClearCache:
    """Test azure_auth --clear-cache flag."""

    def test_clear_cache_exits_0(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "org_ops_tools.shared.azure_auth", "--clear-cache"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_clear_cache_prints_confirmation(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "org_ops_tools.shared.azure_auth", "--clear-cache"],
            capture_output=True,
            text=True,
        )
        assert len(result.stdout.strip()) > 0


class TestAzureAuthHelp:
    """Test azure_auth with no args or --help."""

    def test_help_exits_0(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "org_ops_tools.shared.azure_auth", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_help_shows_usage(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "org_ops_tools.shared.azure_auth", "--help"],
            capture_output=True,
            text=True,
        )
        assert "usage" in result.stdout.lower() or "login" in result.stdout.lower()
