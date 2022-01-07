import pprint

import pytest

from tests.song.models import SongCreate, SongUpdate
from tests.song.services import SongService


@pytest.mark.asyncio
async def test_song_service_create_song(app, sqlalchemy, song_data_one):
    async with sqlalchemy() as session:
        song = await SongService(db=session).create(
            schema_in=SongCreate(**song_data_one)
        )

    assert getattr(song, "id") is not None
    for key, value in song_data_one.items():
        assert getattr(song, key) == song_data_one[key]


@pytest.mark.asyncio
async def test_song_service_update_song(
    app, sqlalchemy, song_one, song_data_two
):
    async with sqlalchemy() as session:
        song = await SongService(db=session).update(
            instance=song_one, schema_in=SongUpdate(**song_data_two)
        )
    assert song.id == song_one.id
    for key, value in song_data_two.items():
        assert getattr(song, key) == song_data_two[key]


@pytest.mark.asyncio
async def test_song_service_get_song(app, sqlalchemy, song_one):
    async with sqlalchemy() as session:
        song = await SongService(db=session).get(id=song_one.id)
    assert song is not None


@pytest.mark.asyncio
async def test_song_service_delete_song(app, sqlalchemy, song_one):
    async with sqlalchemy() as session:
        await SongService(db=session).delete(id=song_one.id)
    async with sqlalchemy() as session:
        song = await SongService(db=session).get(id=song_one.id)
    assert song is None


@pytest.mark.asyncio
async def test_song_service_without_repository(app, sqlalchemy, song_one):
    async with sqlalchemy() as session:
        service = SongService(db=session)
        service.repository = None
        with pytest.raises(ValueError):
            await service.get(id=song_one.id)
