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

    @abstractmethod
    async def get(self, **kwargs):
        """Get and return one instance by filter."""
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, **kwargs):
        """Delete one instance by filter."""
        raise NotImplementedError()
