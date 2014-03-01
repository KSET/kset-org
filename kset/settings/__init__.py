# Try to activate local settings. If it fails, assume we're on development and
# activate dev settings. Note that local.py shouldn't be tracked in the
# repository.

try:
    from .local import *
except ImportError:
    from .dev import *
