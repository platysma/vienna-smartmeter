"""Unofficial Python wrapper for the Wiener Netze Smart Meter private API."""
from importlib.metadata import version

from .client import Smartmeter

try:
    __version__ = version(__name__)
except Exception:  # noqa
    pass

__all__ = ["Smartmeter"]

try:

    from ._async.client import AsyncSmartmeter

    __all__ += ["AsyncSmartmeter"]

except (ImportError, SyntaxError):
    pass
