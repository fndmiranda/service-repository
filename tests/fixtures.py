import pytest

from tests.song.models import SongCreate
from tests.song.services import SongService


@pytest.fixture
def song_data_one():
    return {
        "title": "Song title 1",
        "is_active": True,
    }


@pytest.fixture
def song_data_two():
    return {
        "title": "Song title 2",
        "is_active": False,
    }


@pytest.fixture
async def song_one(sqlalchemy, song_data_one):
    async with sqlalchemy() as session:
        song = await SongService(db=session).create(
            schema_in=SongCreate(**song_data_one)
        )
    return song


@pytest.fixture
def product_data_one():
    return {
        "title": "Product title 1",
        "is_active": True,
    }
