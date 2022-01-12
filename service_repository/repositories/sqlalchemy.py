from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from service_repository.interfaces.repository import RepositoryInterface
from service_repository.pagination import apply_pagination


class RepositorySqlalchemy(RepositoryInterface):
    """Class representing the SQLAlchemy abstract repository."""

    _model = None

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def create(self, schema_in: BaseModel):
        """Create new object and returns the saved object instance."""
        instance = self.model(**schema_in)

        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update(self, instance: BaseModel, schema_in: BaseModel):
        """Update a instance."""
        data = instance.dict()

        for field in data:
            if field in schema_in:
                setattr(instance, field, schema_in[field])

        await self.db.commit()

        return instance

    async def get(self, **kwargs):
        """Get one instance by filter."""
        query = await self.db.execute(select(self.model).filter_by(**kwargs))
        instance = query.scalar_one_or_none()
        await self.db.commit()

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

        query_count = await self.db.execute(
            stmt.with_only_columns(func.count(primary_key))
        )

        total = query_count.scalar_one()

        return total

    async def paginate(self, page: int = 1, per_page: int = 15):
        """Get collection of instances paginated."""
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

        return {
            "items": query.scalars().all(),
            "per_page": pagination.page_size,
            "num_pages": pagination.num_pages,
            "page": pagination.page_number,
            "total": pagination.total_results,
        }

    @property
    def model(self):
        if self._model is None:
            raise ValueError("Model is required, set _model")
        return self._model

    @model.setter
    def model(self, value):
        self._model = value
