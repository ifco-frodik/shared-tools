"""Tests for org_ops_tools.shared.config module."""

from pathlib import Path

import pytest
import yaml


class TestLoadConfigDefaults:
    """Test load_config returns defaults when no config file exists."""

    def test_returns_dict(self) -> None:
        from org_ops_tools.shared.config import load_config

        config = load_config()
        assert isinstance(config, dict)

    def test_has_auth_section(self) -> None:
        from org_ops_tools.shared.config import load_config

        config = load_config()
        assert "auth" in config

    def test_has_sqlmi_section(self) -> None:
        from org_ops_tools.shared.config import load_config

        config = load_config()
        assert "sqlmi" in config

    def test_has_ado_section(self) -> None:
        from org_ops_tools.shared.config import load_config

        config = load_config()
        assert "ado" in config


class TestLoadConfigEnvVar:
    """Test load_config reads from ORG_OPS_TOOLS_CONFIG env var."""

    def test_reads_from_env_var_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        from org_ops_tools.shared.config import load_config

        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump({"auth": {"tenant_id": "test-tenant"}}))
        monkeypatch.setenv("ORG_OPS_TOOLS_CONFIG", str(config_file))

        config = load_config()
        assert config["auth"]["tenant_id"] == "test-tenant"


class TestLoadConfigMerge:
    """Test load_config merges user config with defaults."""

    def test_user_override_preserves_other_sections(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        from org_ops_tools.shared.config import load_config

        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump({"auth": {"tenant_id": "my-tenant"}}))
        monkeypatch.setenv("ORG_OPS_TOOLS_CONFIG", str(config_file))

        config = load_config()
        # auth section overridden
        assert config["auth"]["tenant_id"] == "my-tenant"
        # sqlmi section still has defaults
        assert "sqlmi" in config
        assert isinstance(config["sqlmi"], dict)

    def test_user_partial_override_merges_with_section_defaults(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from org_ops_tools.shared.config import load_config

        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump({"sqlmi": {"server": "my-server.database.windows.net"}}))
        monkeypatch.setenv("ORG_OPS_TOOLS_CONFIG", str(config_file))

        config = load_config()
        # user override applied
        assert config["sqlmi"]["server"] == "my-server.database.windows.net"
        # other fields in sqlmi section still have defaults
        assert "port" in config["sqlmi"]
