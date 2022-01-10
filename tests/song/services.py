from service_layer.services import ServiceLayer
from tests.song.repositories import SongRepository


class SongService(ServiceLayer):
    """Class representing the song service."""

    _repository = SongRepository
