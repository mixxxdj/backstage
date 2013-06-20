#!/usr/bin/env python
from django.core.management import execute_manager


if __name__ == "__main__":
    try:
        from backstage import settings_dev
    except ImportError, err:
        import sys
        sys.stderr.write("Manage import Error\n")
        sys.stderr.write(str(err)+"\n")
        sys.exit(1)

    execute_manager(settings_dev)
