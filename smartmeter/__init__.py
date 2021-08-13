"""Unofficial Python wrapper for the Wiener Netze Smart Meter private API."""
import sys
from importlib.metadata import version

from .client import Smartmeter

try:
    __version__ = version(__name__)
except Exception:
    pass

__all__ = ["Smartmeter"]

try:
    if sys.version_info < (3, 6):
        raise ImportError

    from ._async.client import AsyncSmartmeter

    __all__ += ["AsyncSmartmeter"]

except (ImportError, SyntaxError):
    pass
