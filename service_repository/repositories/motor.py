import logging
import math

from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from service_repository.interfaces.repository import RepositoryInterface

logger = logging.getLogger(__name__)


class BaseRepositoryMotor(RepositoryInterface):
    """Class representing the motor abstract repository."""

    _model = None
    _collection = None

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db: AsyncIOMotorDatabase = db

    async def create(self, schema_in: dict):
        """Create new object and returns the saved object instance."""
        logger.info(
            "Starting create repository with={}".format(
                {
                    "repository": type(self).__name__,
                    "data": schema_in,
                }
            )
        )

        try:
            create_data = self.model(**schema_in).dict()
            collection = self.db.get_collection(self.collection)
            result = await collection.insert_one(create_data)
            instance = await collection.find_one({"_id": result.inserted_id})
            schema_out = self.model(**instance)
            logger.info(
                "Repository created successfully with={}".format(
                    {
                        "repository": type(self).__name__,
                        "data": schema_out.dict(),
                    }
                )
            )
            return schema_out
        except Exception as exc:
            logger.error(
                "Error on create repository with={}".format(
                    {
                        "repository": type(self).__name__,
                        "error": str(exc),
                        "data": schema_in,
                    },
                )
            )
            raise exc

    async def update(self, instance: BaseModel, schema_in: dict):
        """Update a instance."""
        logger.info(
            "Starting update repository with={}".format(
                {
                    "repository": type(self).__name__,
                    "id": instance.id,
                    "data": schema_in,
                }
            )
        )
        update_data = {
            "$set": schema_in,
            "$currentDate": {"updated_at": True},
        }
        try:
            criteria = {"_id": instance.id}
            collection = self.db.get_collection(self.collection)
            await collection.update_one(criteria, update_data)
            instance = await collection.find_one(criteria)
            schema_out = self.model(**instance)
            logger.info(
                "Repository updated successfully with={}".format(
                    {
                        "repository": type(self).__name__,
                        "data": schema_out.dict(),
                    }
                )
            )
            return schema_out
        except Exception as exc:
            logger.error(
                "Error on update repository with={}".format(
                    {
                        "repository": type(self).__name__,
                        "error": str(exc),
                        "data": schema_in,
                    }
                )
            )
            raise exc

    async def get(self, **kwargs):
        """Get one instance by filter."""
        logger.info(
            "Starting get repository with={}".format(
                {
                    "repository": type(self).__name__,
                    "kwargs": kwargs,
                }
            )
        )

        try:
            collection = self.db.get_collection(self.collection)
            instance = await collection.find_one(kwargs)
            if instance:
                schema_out = self.model(**instance)
                logger.info(
                    "Repository got successfully with={}".format(
                        {
                            "repository": type(self).__name__,
                            "kwargs": kwargs,
                        }
                    )
                )
                return schema_out
        except Exception as exc:
            logger.error(
                "Error on get repository with={}".format(
                    {
                        "repository": type(self).__name__,
                        "error": str(exc),
                        "kwargs": kwargs,
                    }
                )
            )
            raise exc

    async def delete(self, **kwargs):
        """Delete one instance by filter."""
        logger.info(
            "Starting delete repository with={}".format(
                {
                    "repository": type(self).__name__,
                    "kwargs": kwargs,
                }
            )
        )
        try:
            collection = self.db.get_collection(self.collection)
            await collection.delete_one(kwargs)
            logger.info(
                "Repository deleted successfully with={}".format(
                    {
                        "repository": type(self).__name__,
                        "kwargs": kwargs,
                    }
                )
            )
        except Exception as exc:
            logger.error(
                "Error on delete repository with={}".format(
                    {
                        "repository": type(self).__name__,
                        "error": str(exc),
                        "kwargs": kwargs,
                    }
                )
            )
            raise exc

    async def count(self, **kwargs):
        """Count instances by filter."""
        logger.info(
            "Starting count repository with={}".format(
                {
                    "repository": type(self).__name__,
                    "kwargs": kwargs,
                }
            )
        )
        try:
            collection = self.db.get_collection(self.collection)
            total = await collection.count_documents(kwargs)
            logger.info(
                "Repository counted successfully with={}".format(
                    {
                        "repository": type(self).__name__,
                        "kwargs": kwargs,
                        "total": total,
                    }
                )
            )
            return total
        except Exception as exc:
            logger.error(
                "Error on count repository with={}".format(
                    {
                        "repository": type(self).__name__,
                        "error": str(exc),
                        "kwargs": kwargs,
                    }
                )
            )
            raise exc

    async def paginate(self, page: int = 1, per_page: int = 15, **kwargs):
        """Get collection of instances paginated by filter."""
        logger.info(
            "Starting paginate repository with={}".format(
                {
                    "repository": type(self).__name__,
                    "kwargs": kwargs,
                    "page": page,
                    "per_page": per_page,
                }
            )
        )
        try:
            collection = self.db.get_collection(self.collection)
            total = await collection.count_documents(kwargs)

            items = (
                await collection.find(**kwargs)
                .skip(per_page * (page - 1))
                .to_list(per_page)
            )

            response = {
                "items": [self.model(**item) for item in items],
                "per_page": per_page,
                "num_pages": int(math.ceil(total / per_page)),
                "page": page,
                "total": total,
            }
            logger.info(
                "Repository paginate successfully with={}".format(
                    {
                        "repository": type(self).__name__,
                        "kwargs": kwargs,
                        "items": len(response["items"]),
                        "per_page": response["per_page"],
                        "num_pages": response["num_pages"],
                        "page": response["page"],
                        "total": response["total"],
                    }
                )
            )
            return response
        except Exception as exc:
            logger.error(
                "Error on paginate repository with={}".format(
                    {
                        "repository": type(self).__name__,
                        "kwargs": kwargs,
                        "page": page,
                        "per_page": per_page,
                    }
                )
            )
            raise exc

    @property
    def model(self) -> BaseModel:
        if self._model is None:
            raise ValueError("Model is required, set _model")
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def collection(self):
        if self._collection is None:
            raise ValueError("Collection is required, set _collection")
        return self._collection

    @collection.setter
    def collection(self, value):
        self._collection = value
