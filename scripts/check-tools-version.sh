#!/bin/bash
# Usage: check-tools-version.sh [minimum-version]
# Checks if org-ops-tools is installed and meets minimum version.
# Exit 0 in all cases -- informational only, does NOT block.

MIN_VERSION="${1:-1.0.0}"

if ! python -c "import org_ops_tools" 2>/dev/null; then
  echo "[ops-tools] WARNING: org-ops-tools is not installed. Run: uv pip install git+https://github.com/ifco-frodik/claude-shared-tools.git@v${MIN_VERSION}"
  exit 0
fi

INSTALLED=$(python -c "import org_ops_tools; print(org_ops_tools.__version__)")

python -c "
from packaging.version import Version
import sys
if Version('${INSTALLED}') < Version('${MIN_VERSION}'):
    print('[ops-tools] WARNING: org-ops-tools ${INSTALLED} is installed but >= ${MIN_VERSION} is required. Run: uv pip install --upgrade git+https://github.com/ifco-frodik/claude-shared-tools.git@v${MIN_VERSION}')
    sys.exit(0)
print('[ops-tools] org-ops-tools ${INSTALLED} OK')
"
