from collections.abc import AsyncIterator

import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient

from litestar_todo.main.app import app

app.debug = True


@pytest.fixture
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Yields a test client."""
    async with AsyncTestClient(app=app) as client:
        yield client


async def test_without_any_sense(
    test_client: AsyncTestClient[Litestar],
) -> None:
    """Test the root endpoint."""
    assert test_client.app is not None
