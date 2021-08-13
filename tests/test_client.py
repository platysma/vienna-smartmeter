"""Test cases for Smartmeter client."""

from smartmeter.client import Smartmeter
from tests.const import DEMO_PASSWORD, DEMO_USERNAME
import pytest

from datetime import datetime


@pytest.fixture()
def client():
    """Log in to Smartmeter session fixture."""
    client = Smartmeter(DEMO_USERNAME, DEMO_PASSWORD)
    yield client
    client.session.close()


def test_confirm_login(client):
    """Tests if login is successful."""
    assert len(client.profil()) > 0


def test_zaehlpunkte(client):
    """Tests if any zaehkpunkte exist."""
    zp = client.zaehlpunkte()
    assert len(zp) > 0
    assert len(zp[0]["zaehlpunkte"]) > 0


def test_ereignisse(client):
    """Tests if ereignisse exist."""
    eg_query = client.ereignisse(datetime(2021, 1, 1), datetime(2021, 1, 2))
    assert len(eg_query) == 1
    assert eg_query[0]["name"] == "Wäsche waschen"
