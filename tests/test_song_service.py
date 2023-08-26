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
async def test_song_service_paginate_song(app, sqlalchemy, song_data_one):
    count = 15
    async with sqlalchemy() as session:
        for item in range(count):
            song_data_one.update(
                {
                    "title": f"Song title {item}",
                }
            )

            await SongService(db=session).create(
                schema_in=SongCreate(**song_data_one)
            )

    async with sqlalchemy() as session:
        pagination = await SongService(db=session).paginate(page=1, per_page=5)

    assert pagination["per_page"] == 5
    assert len(pagination["items"]) == 5
    assert pagination["num_pages"] == 3
    assert pagination["page"] == 1
    assert pagination["total"] == 15


@pytest.mark.asyncio
async def test_song_service_with_filter_paginate_song(
    app, sqlalchemy, song_data_one
):
    count = 15
    criteria = [{"field": "title", "op": "ilike", "value": "Song title 1"}]

    async with sqlalchemy() as session:
        for item in range(count):
            song_data_one.update(
                {
                    "title": f"Song title {item}",
                }
            )

            await SongService(db=session).create(
                schema_in=SongCreate(**song_data_one)
            )

    async with sqlalchemy() as session:
        pagination = await SongService(db=session).paginate(
            page=1, per_page=5, criteria=criteria
        )

    assert pagination["per_page"] == 5
    assert len(pagination["items"]) == 1
    assert pagination["num_pages"] == 1
    assert pagination["page"] == 1
    assert pagination["total"] == 1


@pytest.mark.asyncio
async def test_song_service_with_or_filter_paginate_song(
    app, sqlalchemy, song_data_one
):
    count = 15

    criteria = {
        "or": [
            {"field": "title", "op": "==", "value": "Song title 2"},
            {"field": "title", "op": "==", "value": "Song title 3"},
        ]
    }

    async with sqlalchemy() as session:
        for item in range(count):
            song_data_one.update(
                {
                    "title": f"Song title {item}",
                }
            )

            await SongService(db=session).create(
                schema_in=SongCreate(**song_data_one)
            )

    async with sqlalchemy() as session:
        pagination = await SongService(db=session).paginate(
            page=1, per_page=5, criteria=criteria
        )

    assert pagination["per_page"] == 5
    assert len(pagination["items"]) == 2
    assert pagination["num_pages"] == 1
    assert pagination["page"] == 1
    assert pagination["total"] == 2


@pytest.mark.asyncio
async def test_song_service_with_or_and_asc_filter_paginate_song(
    app, sqlalchemy, song_data_one
):
    count = 15
    criteria = {
        "or": [
            {"field": "title", "op": "==", "value": "Song title 2"},
            {"field": "title", "op": "==", "value": "Song title 3"},
        ]
    }
    sort = [
        {"field": "title", "direction": "asc"},
    ]

    async with sqlalchemy() as session:
        for item in range(count):
            song_data_one.update(
                {
                    "title": f"Song title {item}",
                }
            )

            await SongService(db=session).create(
                schema_in=SongCreate(**song_data_one)
            )

    async with sqlalchemy() as session:
        pagination = await SongService(db=session).paginate(
            page=1, per_page=5, criteria=criteria, sort=sort
        )

    assert pagination["items"][0].title == "Song title 2"


@pytest.mark.asyncio
async def test_song_service_with_or_and_desc_filter_paginate_song(
    app, sqlalchemy, song_data_one
):
    count = 15
    criteria = {
        "or": [
            {"field": "title", "op": "==", "value": "Song title 2"},
            {"field": "title", "op": "==", "value": "Song title 3"},
        ]
    }
    sort = [
        {"field": "title", "direction": "desc"},
    ]

    async with sqlalchemy() as session:
        for item in range(count):
            song_data_one.update(
                {
                    "title": f"Song title {item}",
                }
            )

            await SongService(db=session).create(
                schema_in=SongCreate(**song_data_one)
            )

    async with sqlalchemy() as session:
        pagination = await SongService(db=session).paginate(
            page=1, per_page=5, criteria=criteria, sort=sort
        )

    assert pagination["items"][0].title == "Song title 3"


@pytest.mark.asyncio
async def test_song_service_get_all_songs(app, sqlalchemy, song_data_one):
    count = 5
    async with sqlalchemy() as session:
        for item in range(count):
            song_data_one.update(
                {
                    "title": f"Song title {item}",
                }
            )

            await SongService(db=session).create(
                schema_in=SongCreate(**song_data_one)
            )

    async with sqlalchemy() as session:
        songs = await SongService(db=session).all()

    assert len(songs) == count


@pytest.mark.asyncio
async def test_song_service_get_all_songs_with_filter(
    app, sqlalchemy, song_data_one
):
    count = 5
    async with sqlalchemy() as session:
        for item in range(count):
            song_data_one.update(
                {
                    "title": f"Song title {item}",
                }
            )

            await SongService(db=session).create(
                schema_in=SongCreate(**song_data_one)
            )

    async with sqlalchemy() as session:
        songs = await SongService(db=session).all(title="Song title 1")

    assert len(songs) == 1


@pytest.mark.asyncio
async def test_song_service_delete_song(app, sqlalchemy, song_one):
    async with sqlalchemy() as session:
        await SongService(db=session).delete(id=song_one.id)
    async with sqlalchemy() as session:
        song = await SongService(db=session).get(id=song_one.id)
    assert song is None


@pytest.mark.asyncio
async def test_song_service_count_song(app, sqlalchemy, song_data_one):
    count = 5
    async with sqlalchemy() as session:
        for item in range(count):
            song_data_one.update(
                {
                    "title": f"Song title {item}",
                }
            )

            await SongService(db=session).create(
                schema_in=SongCreate(**song_data_one)
            )

    async with sqlalchemy() as session:
        total = await SongService(db=session).count()

    assert total == count
