from service_layer.repositories.sqlalchemy import AbstractRepositorySqlalchemy
from tests.song.models import Song


class SongRepository(AbstractRepositorySqlalchemy):
    """Class representing the song repository."""

    _model = Song
