from service_repository.repositories.sqlalchemy import BaseRepositorySqlalchemy
from tests.song.models import Song


class SongRepository(BaseRepositorySqlalchemy):
    """Class representing the song repository."""

    model = Song
