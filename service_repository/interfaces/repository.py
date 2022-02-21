from abc import ABCMeta, abstractmethod

from pydantic import BaseModel


class RepositoryInterface(metaclass=ABCMeta):
    """Class representing the repository interface."""

    @abstractmethod
    async def create(self, schema_in: dict):
        """
        Create new entity and returns the saved instance.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, instance: BaseModel, schema_in: dict):
        """Updates an entity and returns the saved instance."""
        raise NotImplementedError()

    @abstractmethod
    async def get(self, **kwargs):
        """Get and return one instance by filter."""
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, **kwargs):
        """Delete one instance by filter."""
        raise NotImplementedError()
