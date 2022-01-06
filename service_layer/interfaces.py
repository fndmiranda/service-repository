from abc import ABCMeta, abstractmethod

from pydantic import BaseModel


class ServiceInterface(metaclass=ABCMeta):
    """Class representing the service interface."""

    @abstractmethod
    async def create(self, schema_in: BaseModel):
        """
        Create new entity and returns the saved instance.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, instance: BaseModel, schema_in: BaseModel):
        """Updates an entity and returns the saved instance."""
        raise NotImplementedError()


class RepositoryInterface(metaclass=ABCMeta):
    """Class representing the repository interface."""

    @abstractmethod
    async def create(self, schema_in: BaseModel):
        """
        Create new entity and returns the saved instance.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, instance: BaseModel, schema_in: BaseModel):
        """Updates an entity and returns the saved instance."""
        raise NotImplementedError()
