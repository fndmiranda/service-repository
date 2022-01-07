import pprint
from typing import List

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from service_layer.interfaces import ServiceInterface


class AbstractService(ServiceInterface):
    """Class representing the abstract service."""

    _repository = None

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def create(self, schema_in: BaseModel):
        """
        Create new entity and returns the saved entity instance.
        """
        create_data = schema_in.dict()
        instance = await self.repository(db=self.db).create(
            schema_in=create_data
        )
        return instance

    async def update(self, instance: BaseModel, schema_in: BaseModel):
        """Update a instance."""
        update_data = schema_in.dict(exclude_unset=True)
        instance = await self.repository(db=self.db).update(
            instance=instance, schema_in=update_data
        )
        return instance

    # async def paginate(
    #     self,
    #     page: int = 1,
    #     items_per_page: int = 15,
    #     filter_spec: List[dict] = None,
    #     sort_spec: List[str] = None,
    # ):
    #     """
    #     Common functionality for searching, filtering, sorting, and pagination.
    #     """
    #     pagination = await self.repository(db=self.db).paginate(
    #         page=page,
    #         items_per_page=items_per_page,
    #         filter_spec=filter_spec,
    #         sort_spec=sort_spec,
    #     )
    #     return pagination

    async def get(self, **kwargs):
        """Get one instance by filter."""
        instance = await self.repository(db=self.db).get(**kwargs)
        return instance

    # async def get_or_404(self, **kwargs):
    #     """Get one instance by filter or 404 if not exists."""
    #     instance = await self.get(**kwargs)
    #     if not instance:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #     return instance

    # async def update_or_404(self, schema_in: BaseModel, **kwargs):
    #     """Update instance or 404 if not exists."""
    #     instance = await self.get_or_404(**kwargs)
    #     instance = await self.update(instance=instance, schema_in=schema_in)
    #     return instance

    async def delete(self, **kwargs):
        """Delete one instance by filter."""
        instance = await self.get(**kwargs)
        await self.db.delete(instance)
        await self.db.commit()

    # async def delete_or_404(self, **kwargs):
    #     """Delete one instance by filter or 404 if not exists."""
    #     instance = await self.get_or_404(**kwargs)
    #     await self.db.delete(instance)
    #     await self.db.commit()

    @property
    def repository(self):
        if self._repository is None:
            raise ValueError("Repository is required, set _repository")
        return self._repository

    @repository.setter
    def repository(self, value):
        self._repository = value
