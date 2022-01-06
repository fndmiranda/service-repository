from service_layer.services import AbstractService
from tests.song.repositories import SongRepository


class SongService(AbstractService):
    """Class representing the song service."""

    _repository = SongRepository
