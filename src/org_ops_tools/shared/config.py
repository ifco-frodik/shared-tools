"""Configuration reader for org-ops-tools.

Reads config.yaml from ~/.org-ops-tools/ or ORG_OPS_TOOLS_CONFIG env var.
Returns sensible defaults when no config file exists.
"""

from __future__ import annotations

import copy
import os
from pathlib import Path

import yaml

DEFAULT_CONFIG_DIR = Path.home() / ".org-ops-tools"

DEFAULT_CONFIG: dict[str, dict[str, object]] = {
    "auth": {"tenant_id": "", "client_id": "", "preferred_flow": "interactive"},
    "sqlmi": {"server": "", "database": "", "port": 1433},
    "ado": {"organization": "", "default_project": ""},
}


def load_config() -> dict[str, dict[str, object]]:
    """Load config from YAML file, falling back to defaults.

    Config file location priority:
    1. ORG_OPS_TOOLS_CONFIG environment variable
    2. ~/.org-ops-tools/config.yaml
    3. Built-in defaults (if no file exists)
    """
    config_path = os.environ.get("ORG_OPS_TOOLS_CONFIG")
    config_file = Path(config_path) if config_path else DEFAULT_CONFIG_DIR / "config.yaml"

    if config_file.exists():
        with open(config_file) as f:
            user_config = yaml.safe_load(f) or {}
        # Merge with defaults section by section
        merged = copy.deepcopy(DEFAULT_CONFIG)
        for key in DEFAULT_CONFIG:
            if key in user_config and isinstance(user_config[key], dict):
                merged[key] = {**DEFAULT_CONFIG[key], **user_config[key]}
        return merged

    return copy.deepcopy(DEFAULT_CONFIG)
