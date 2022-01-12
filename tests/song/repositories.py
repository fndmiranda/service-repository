from service_repository.repositories.sqlalchemy import RepositorySqlalchemy
from tests.song.models import Song


class SongRepository(RepositorySqlalchemy):
    """Class representing the song repository."""

    _model = Song
