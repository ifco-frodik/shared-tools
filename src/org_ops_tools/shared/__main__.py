"""Entry point for python -m org_ops_tools.shared.

Delegates to azure_auth CLI by default.
"""

from org_ops_tools.shared.azure_auth import main

if __name__ == "__main__":
    main()
