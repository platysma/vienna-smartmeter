"""Test cases for Smartmeter client."""

from smartmeter._async.client import AsyncSmartmeter
from tests.const import DEMO_PASSWORD, DEMO_USERNAME
import pytest


@pytest.fixture()
async def client():
    """Log in to Smartmeter session fixture."""
    client = AsyncSmartmeter(DEMO_USERNAME, DEMO_PASSWORD)
    await client.refresh_token()
    yield client
    await client._session.close()


@pytest.mark.asyncio
async def test_confirm_login(client):
    """Tests if login is successful."""
    assert len(await client.profil()) > 0