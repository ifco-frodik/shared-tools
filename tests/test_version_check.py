"""Tests for check-tools-version.sh script."""

import subprocess
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "check-tools-version.sh"
PYTHON = Path(__file__).parent.parent / ".venv" / "bin" / "python"


def test_version_check_installed_ok() -> None:
    """When package installed and version >= minimum, prints OK, exits 0."""
    result = subprocess.run(
        ["bash", str(SCRIPT_PATH), "1.0.0"],
        capture_output=True,
        text=True,
        env={"PATH": str(PYTHON.parent) + ":/usr/bin:/bin"},
    )
    assert result.returncode == 0
    assert "OK" in result.stdout


def test_version_check_version_too_low() -> None:
    """When package installed but version < minimum, prints WARNING, exits 0."""
    result = subprocess.run(
        ["bash", str(SCRIPT_PATH), "99.0.0"],
        capture_output=True,
        text=True,
        env={"PATH": str(PYTHON.parent) + ":/usr/bin:/bin"},
    )
    assert result.returncode == 0
    assert "WARNING" in result.stdout


def test_version_check_default_minimum() -> None:
    """When no argument provided, uses default minimum 1.0.0 and exits 0."""
    result = subprocess.run(
        ["bash", str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
        env={"PATH": str(PYTHON.parent) + ":/usr/bin:/bin"},
    )
    assert result.returncode == 0
