# Import the proper settings based on active.py
from .env.active import *

# Import local dev settings
try:
    from .local import *
except ImportError:
    pass
