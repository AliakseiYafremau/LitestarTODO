from collections.abc import AsyncIterator

import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

from litestar_template.main.app import app

app.debug = True


@pytest.fixture
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Yields a test client."""
    async with AsyncTestClient(app=app) as client:
        yield client


async def test_list_lists(test_client: AsyncTestClient[Litestar]) -> None:
    """Test get /list/all."""
    response = await test_client.get("/list/all")
    assert response.status_code == HTTP_200_OK
