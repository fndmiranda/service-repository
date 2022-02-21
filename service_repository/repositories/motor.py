import math

from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from service_repository.interfaces.repository import RepositoryInterface


class BaseRepositoryMotor(RepositoryInterface):
    """Class representing the motor abstract repository."""

    _model = None
    _collection = None

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db: AsyncIOMotorDatabase = db

    async def create(self, schema_in: dict):
        """Create new object and returns the saved object instance."""
        create_data = self.model(**schema_in).dict()
        collection = self.db.get_collection(self.collection)
        result = await collection.insert_one(create_data)
        instance = await collection.find_one({"_id": result.inserted_id})
        schema_out = self.model(**instance)
        return schema_out

    async def update(self, instance: BaseModel, schema_in: dict):
        """Update a instance."""
        update_data = {
            "$set": schema_in,
            "$currentDate": {"updated_at": True},
        }
        criteria = {"_id": instance.id}
        collection = self.db.get_collection(self.collection)
        await collection.update_one(criteria, update_data)
        instance = await collection.find_one(criteria)
        schema_out = self.model(**instance)
        return schema_out

    async def get(self, **kwargs):
        """Get one instance by filter."""
        collection = self.db.get_collection(self.collection)
        instance = await collection.find_one(kwargs)
        if instance:
            schema_out = self.model(**instance)
            return schema_out

    async def delete(self, **kwargs):
        """Delete one instance by filter."""
        collection = self.db.get_collection(self.collection)
        await collection.delete_one(kwargs)

    async def count(self, **kwargs):
        """Count instances by filter."""
        collection = self.db.get_collection(self.collection)
        total = await collection.count_documents(kwargs)
        return total

    async def paginate(
        self,
        page: int = 1,
        per_page: int = 15,
        criteria: dict = {},
        sort: list = [],
    ):
        """Get collection of instances paginated by filter."""
        collection = self.db.get_collection(self.collection)
        total = await collection.count_documents(criteria)
        items = collection.find(criteria)

        if sort:
            items = items.sort(sort)

        items = await items.to_list(per_page)

        response = {
            "items": [self.model(**item) for item in items],
            "per_page": per_page,
            "num_pages": int(math.ceil(total / per_page)),
            "page": page,
            "total": total,
        }
        return response

    @property
    def model(self):
        if self._model is None:
            raise ValueError("Model is None, set the model")
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def collection(self):
        if self._collection is None:
            raise ValueError("Collection is None, set the collection")
        return self._collection

    @collection.setter
    def collection(self, value):
        self._collection = value
