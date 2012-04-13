from __future__ import absolute_import
import os

if 'PROD' in os.environ:
    from .production import *
else:
    from .dev import *

