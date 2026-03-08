# org-ops-tools

CLI tools for ops monitoring -- SQLMI queries, Azure DevOps pipelines, and Azure DevOps repos. Mock implementations for POC; designed for easy swap to real Azure integrations.

## Installation

```bash
uv pip install git+https://github.com/ifco-frodik/claude-shared-tools.git@v1.0.0
```

## Usage

All tools are invoked via `python -m` and output JSON to stdout by default.

### SQLMI Queries

```bash
# Query critical alerts
python -m org_ops_tools.sqlmi --preset critical-alerts

# Query recent queries
python -m org_ops_tools.sqlmi --preset recent-queries

# Performance summary
python -m org_ops_tools.sqlmi --preset performance-summary

# Table output
python -m org_ops_tools.sqlmi --preset critical-alerts --format table
```

### ADO Pipelines

```bash
# List pipeline runs (default: all)
python -m org_ops_tools.ado_pipelines runs

# Filter by status
python -m org_ops_tools.ado_pipelines runs --status failed

# View logs for a specific run
python -m org_ops_tools.ado_pipelines logs --run-id 1001

# Pipeline summary
python -m org_ops_tools.ado_pipelines summary
```

### ADO Repos

```bash
# List active pull requests
python -m org_ops_tools.ado_repos prs --status active

# Scan repos
python -m org_ops_tools.ado_repos scan

# View branch policies
python -m org_ops_tools.ado_repos policies
```

### Authentication

```bash
# Login (mock -- prints success message)
python -m org_ops_tools.shared.azure_auth --login

# Check auth status
python -m org_ops_tools.shared.azure_auth --status

# Clear cached credentials
python -m org_ops_tools.shared.azure_auth --clear-cache
```

## Output Format

All tools support `--format json|table` (default: `json`).

- **json**: Pretty-printed JSON to stdout (indent=2)
- **table**: Human-readable table to stdout

## Error Handling

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid arguments, unknown preset, etc.) |
| 2 | Authentication failure |

### Error Output

Errors are written to stderr as JSON:

```json
{"status": "error", "error": "description of the problem"}
```

## Version Check

A shell script is included for plugin SessionStart hooks to verify the tools package is installed and up-to-date:

```bash
bash scripts/check-tools-version.sh 1.0.0
```

The script is informational only -- it always exits 0 and prints either an OK message or a WARNING with install/upgrade instructions.

## Configuration

Tools read configuration from `~/.org-ops-tools/config.yaml`. Override the config path with the `ORG_OPS_TOOLS_CONFIG` environment variable:

```bash
export ORG_OPS_TOOLS_CONFIG=/path/to/custom/config.yaml
```

Default configuration is used when no config file exists. See the config module for the full default structure.

## Development

### Setup

```bash
cd shared-tools
uv pip install -e ".[dev]"
```

### Running Tests

```bash
make test
```

### Linting

```bash
make lint
```

### Type Checking

```bash
make typecheck
```

### Full Validation

```bash
make validate
```

This runs lint (ruff), typecheck (mypy), and test (pytest) in sequence.
