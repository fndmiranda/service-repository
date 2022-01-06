import pytest

from service_layer import __version__


@pytest.mark.asyncio
async def test_version():
    assert __version__ == "0.1.0"
