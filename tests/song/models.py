from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from tests.utils import uuid_generate


class SongBase(SQLModel):
    title: str = Field(default=None, min_length=1, max_length=64)
    is_active: Optional[bool] = True


class Song(SongBase, table=True):
    id: UUID = Field(default_factory=uuid_generate, primary_key=True)


class SongCreate(SongBase):
    title: str


class SongUpdate(SongBase):
    pass
