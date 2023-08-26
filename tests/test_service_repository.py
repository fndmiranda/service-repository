import pytest

from service_repository import __version__


@pytest.mark.asyncio
async def test_version():
    assert __version__ == "0.2.0"
