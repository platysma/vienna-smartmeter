"""Test cases for Smartmeter client."""
import pytest
from tests.const import DEMO_PASSWORD
from tests.const import DEMO_USERNAME

from smartmeter._async.client import AsyncSmartmeter


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


@pytest.mark.asyncio
async def test_zaehlpunkte(client):
    """Tests if any zaehlpunkte exist."""
    zp = await client.zaehlpunkte()
    assert len(zp) > 0
    assert len(zp[0]["zaehlpunkte"]) > 0
