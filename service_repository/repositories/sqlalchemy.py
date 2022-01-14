import logging

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from service_repository.interfaces.repository import RepositoryInterface
from service_repository.pagination import apply_pagination

logger = logging.getLogger(__name__)


class BaseRepositorySqlalchemy(RepositoryInterface):
    """Class representing the SQLAlchemy abstract repository."""

    _model = None

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

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
            instance = self.model(**schema_in)
            self.db.add(instance)
            await self.db.commit()
            await self.db.refresh(instance)
            logger.info(
                "Repository created successfully with={}".format(
                    {
                        "repository": type(self).__name__,
                        "data": instance.dict(),
                    }
                )
            )
            return instance
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

        try:
            data = instance.dict()

            for field in data:
                if field in schema_in:
                    setattr(instance, field, schema_in[field])

            await self.db.commit()

            logger.info(
                "Repository updated successfully with={}".format(
                    {
                        "repository": type(self).__name__,
                        "data": instance.dict(),
                    }
                )
            )

            return instance
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
            query = await self.db.execute(
                select(self.model).filter_by(**kwargs)
            )
            instance = query.scalar_one_or_none()
            await self.db.commit()

            if instance:
                logger.info(
                    "Repository got successfully with={}".format(
                        {
                            "repository": type(self).__name__,
                            "kwargs": kwargs,
                            "data": instance.dict(),
                        }
                    )
                )
                return instance
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
            instance = await self.get(**kwargs)
            await self.db.delete(instance)
            await self.db.commit()
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
            primary_key = getattr(
                self.model,
                self.model.__table__.primary_key.columns_autoinc_first[0].name,
            )

            stmt = select(self.model)

            query_count = await self.db.execute(
                stmt.with_only_columns(func.count(primary_key))
            )

            total = query_count.scalar_one()
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
            stmt = select(self.model)

            if per_page == -1:
                per_page = None

            stmt, pagination = await apply_pagination(
                stmt,
                session=self.db,
                model=self.model,
                page_number=page,
                page_size=per_page,
            )

            query = await self.db.execute(stmt)
            await self.db.commit()

            response = {
                "items": query.scalars().all(),
                "per_page": pagination.page_size,
                "num_pages": pagination.num_pages,
                "page": pagination.page_number,
                "total": pagination.total_results,
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
    def model(self):
        if self._model is None:
            raise ValueError("Model is required, set _model")
        return self._model

    @model.setter
    def model(self, value):
        self._model = value
