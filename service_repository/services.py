import logging

from pydantic import BaseModel

from service_repository.interfaces.service import ServiceInterface

logger = logging.getLogger(__name__)


class BaseService(ServiceInterface):
    """Class representing the abstract service."""

    class Config:
        repository = None

    def __init__(self, db) -> None:
        self.db = db

    async def create(self, schema_in: BaseModel):
        """
        Create new entity and returns the saved entity instance.
        """
        create_data = schema_in.dict()
        logger.info(
            "Starting create model with={}".format(
                {
                    "service": type(self).__name__,
                    "repository": self.repository.__name__,
                    "create_data": create_data,
                }
            )
        )
        try:
            instance = await self.repository(db=self.db).create(
                schema_in=create_data
            )
            logger.info(
                "Model created successfully with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "create_data": create_data,
                        "schema_out": instance.dict(),
                    }
                )
            )

            return instance
        except Exception as exc:
            logger.error(
                "Error on create model with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "error": str(exc),
                        "create_data": create_data,
                    },
                )
            )
            raise exc

    async def update(self, instance: BaseModel, schema_in: BaseModel):
        """Update a instance."""
        update_data = schema_in.dict(exclude_unset=True)
        logger.info(
            "Starting update model with={}".format(
                {
                    "service": type(self).__name__,
                    "repository": self.repository.__name__,
                    "id": getattr(instance, "id"),
                    "update_data": update_data,
                }
            )
        )
        try:
            instance = await self.repository(db=self.db).update(
                instance=instance, schema_in=update_data
            )
            logger.info(
                "Model updated successfully with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "id": instance.id,
                        "schema_out": instance.dict(),
                    }
                )
            )
            return instance
        except Exception as exc:
            logger.error(
                "Error on update model with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "id": getattr(instance, "id"),
                        "error": str(exc),
                        "update_data": update_data,
                    }
                )
            )
            raise exc

    async def get(self, **kwargs):
        """Get one instance by filter."""
        logger.info(
            "Starting get one model with={}".format(
                {
                    "service": type(self).__name__,
                    "repository": self.repository.__name__,
                    "kwargs": kwargs,
                }
            )
        )
        try:
            instance = await self.repository(db=self.db).get(**kwargs)
            if instance:
                logger.info(
                    "Model got successfully with={}".format(
                        {
                            "service": type(self).__name__,
                            "repository": self.repository.__name__,
                            "kwargs": kwargs,
                            "schema_out": instance.dict(),
                        }
                    )
                )
                return instance
        except Exception as exc:
            logger.error(
                "Error on get one model with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "error": str(exc),
                        "kwargs": kwargs,
                    }
                )
            )
            raise exc

    async def delete(self, **kwargs):
        """Delete one instance by filter."""
        logger.info(
            "Starting delete one model with={}".format(
                {
                    "service": type(self).__name__,
                    "repository": self.repository.__name__,
                    "kwargs": kwargs,
                }
            )
        )
        try:
            await self.repository(db=self.db).delete(**kwargs)
            logger.info(
                "Model deleted successfully with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "kwargs": kwargs,
                    }
                )
            )
        except Exception as exc:
            logger.error(
                "Error on delete one model with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "error": str(exc),
                        "kwargs": kwargs,
                    }
                )
            )
            raise exc

    async def count(self, **kwargs):
        """Count instances by filter."""
        logger.info(
            "Starting count model with={}".format(
                {
                    "service": type(self).__name__,
                    "repository": self.repository.__name__,
                    "kwargs": kwargs,
                }
            )
        )
        try:
            total = await self.repository(db=self.db).count(**kwargs)
            logger.info(
                "Models counted successfully with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "kwargs": kwargs,
                        "total": total,
                    }
                )
            )
            return total
        except Exception as exc:
            logger.error(
                "Error on count model with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "error": str(exc),
                        "kwargs": kwargs,
                    }
                )
            )
            raise exc

    async def paginate(self, page: int = 1, per_page: int = 15, **kwargs):
        """Get collection of instances paginated by filter."""
        logger.info(
            "Starting paginate models with={}".format(
                {
                    "service": type(self).__name__,
                    "repository": self.repository.__name__,
                    "kwargs": kwargs,
                    "page": page,
                    "per_page": per_page,
                }
            )
        )
        try:
            pagination = await self.repository(db=self.db).paginate(
                page=page,
                per_page=per_page,
            )
            logger.info(
                "Models paginate successfully with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "kwargs": kwargs,
                        "items": len(pagination["items"]),
                        "per_page": pagination["per_page"],
                        "num_pages": pagination["num_pages"],
                        "page": pagination["page"],
                        "total": pagination["total"],
                    }
                )
            )
            return pagination
        except Exception as exc:
            logger.error(
                "Error on paginate models with={}".format(
                    {
                        "service": type(self).__name__,
                        "repository": self.repository.__name__,
                        "kwargs": kwargs,
                        "page": page,
                        "per_page": per_page,
                    }
                )
            )
            raise exc

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

    # async def delete_or_404(self, **kwargs):
    #     """Delete one instance by filter or 404 if not exists."""
    #     instance = await self.get_or_404(**kwargs)
    #     await self.db.delete(instance)
    #     await self.db.commit()

    @property
    def repository(self):
        if self.Config.repository is None:
            raise ValueError("Repository is None, set repository in Config")
        return self.Config.repository

    @repository.setter
    def repository(self, value):
        self.Config.repository = value
