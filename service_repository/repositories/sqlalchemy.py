import logging

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from service_repository.filters.filters import apply_filters
from service_repository.filters.pagination import apply_pagination
from service_repository.filters.sorting import apply_sort
from service_repository.interfaces.repository import RepositoryInterface

logger = logging.getLogger(__name__)


class BaseRepositorySqlalchemy(RepositoryInterface):
    """Class representing the SQLAlchemy abstract repository."""

    _model = None
    max_per_page = 25

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def create(self, schema_in: dict, autocommit: bool = True):
        """Create new object and returns the saved object instance."""
        instance = self.model(**schema_in)
        self.db.add(instance)
        if autocommit:
            await self.db.commit()
            await self.db.refresh(instance)
        return instance

    async def update(
        self, instance: BaseModel, schema_in: dict, autocommit: bool = True
    ):
        """Update a instance."""
        data = instance.dict()

        for field in data:
            if field in schema_in:
                setattr(instance, field, schema_in[field])

        if autocommit:
            await self.db.commit()
        return instance

    async def get(self, **kwargs):
        """Get one instance by filter."""
        query = await self.db.execute(select(self.model).filter_by(**kwargs))
        instance = query.scalar_one_or_none()
        await self.db.commit()

        if instance:
            return instance

    async def delete(self, **kwargs):
        """Delete one instance by filter."""
        instance = await self.get(**kwargs)
        await self.db.delete(instance)
        await self.db.commit()

    async def count(self, **kwargs):
        """Count instances by filter."""
        primary_key = getattr(
            self.model,
            self.model.__table__.primary_key.columns_autoinc_first[0].name,
        )

        stmt = select(self.model)

        count = await self.db.execute(
            stmt.with_only_columns(func.count(primary_key)).filter_by(**kwargs)
        )

        total = count.scalar_one()
        return total

    async def paginate(
        self,
        page: int = 1,
        per_page: int = 15,
        criteria: dict = {},
        sort: list = [],
    ):
        """Get collection of instances paginated by filter."""
        if per_page == -1:
            per_page = None
        elif per_page > self.max_per_page:
            per_page = self.max_per_page

        stmt = select(self.model)

        if criteria:
            stmt = apply_filters(stmt, criteria)

        if sort:
            stmt = apply_sort(stmt, sort)

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
            "per_page": per_page,
            "num_pages": pagination.num_pages,
            "page": pagination.page_number,
            "total": pagination.total_results,
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
