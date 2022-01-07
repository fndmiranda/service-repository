import pprint

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from service_layer.interfaces import RepositoryInterface


class AbstractRepositoryMotor(RepositoryInterface):
    """Class representing the motor abstract repository."""

    _model = None
    _collection = None

    def __init__(self, db) -> None:
        self.db = db

    async def create(self, schema_in: BaseModel):
        """Create new object and returns the saved object instance."""
        create_data = self.model(**schema_in).dict()
        collection = self.db.get_collection(self.collection)

        result = await collection.insert_one(create_data)

        instance = await collection.find_one({"_id": result.inserted_id})

        pprint.pp("********************")
        pprint.pp("********************")
        pprint.pp(type(self.db))
        pprint.pp(self.db)
        pprint.pp(type(collection))
        pprint.pp(collection)
        pprint.pp(instance)

        # self.db.add(instance)
        # await self.db.commit()
        # await self.db.refresh(instance)
        return instance

    async def update(self, instance: BaseModel, schema_in: BaseModel):
        """Update a instance."""
        data = jsonable_encoder(instance)

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

    # async def paginate(
    #     self,
    #     page: int = 1,
    #     items_per_page: int = 15,
    # ):
    #     """Common functionality for
    #     searching, filtering, sorting, and pagination."""
    #     stmt = select(self.model)
    #
    #     # if filter_spec:
    #     #     stmt = apply_filters(stmt, filter_spec)
    #     #
    #     # if sort_spec:
    #     #     stmt = apply_sort(stmt, sort_spec)
    #
    #     if items_per_page == -1:
    #         items_per_page = None
    #     elif items_per_page > get_settings().MAX_ITEMS_PER_PAGE:
    #         items_per_page = get_settings().MAX_ITEMS_PER_PAGE
    #
    #     stmt, pagination = await apply_pagination(
    #         stmt,
    #         session=self.db,
    #         model=self.model,
    #         page_number=page,
    #         page_size=items_per_page,
    #     )
    #
    #     query = await self.db.execute(stmt)
    #     await self.db.commit()
    #
    #     return {
    #         "items": query.scalars().all(),
    #         "per_page": pagination.page_size,
    #         "num_pages": pagination.num_pages,
    #         "page": pagination.page_number,
    #         "total": pagination.total_results,
    #     }

    @property
    def model(self):
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
