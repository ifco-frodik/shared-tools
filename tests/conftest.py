"""Shared test fixtures for org-ops-tools."""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def tmp_config(tmp_path: Path) -> Path:
    """Return a temporary directory for config file tests."""
    return tmp_path


def run_module(module: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Run a python -m command and return the result."""
    cmd = [sys.executable, "-m", module, *args]
    return subprocess.run(cmd, capture_output=True, text=True)
