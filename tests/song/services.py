from service_repository.services import BaseService
from tests.song.repositories import SongRepository


class SongService(BaseService):
    """Class representing the song service."""

    class Config:
        repository = SongRepository
