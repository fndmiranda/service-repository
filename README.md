# Abstract service layer built into the repository pattern for SQLAlchemy or MongoDB (asynchronous)

Asynchronous abstract methods for service layer built into the repository pattern for SQLAlchemy or MongoDB with the same service layer.

Inherit the usual service methods:
`pagination`, `create`, `get`, `update`, `delete`, `count`

## Installation

<div class="termy">

```console
$ pip install service-repository

---> 100%
```

</div>

## With SQLAlchemy

Create the model, as in the example [song/models.py](tests/song/models.py)

Create and extend of `BaseRepositorySqlalchemy` in you repository, as in the example [song/repositories.py](tests/song/repositories.py)

Create and extend you service, as in the example [song/services.py](tests/song/services.py)

The following is an example with the connection session, but pass the session as needed.

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel


# Get you connection session of SQLAlchemy, example next, but make as you
@pytest.fixture()
async def sqlalchemy():
    SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///./tests/testing.db"
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URI, future=True, echo=True
    )
    async_session = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        yield async_session
        await conn.run_sync(SQLModel.metadata.drop_all)
```

The following is an example with register created.

```python
import pytest
from tests.song.services import SongService
from tests.song.models import SongCreate


@pytest.fixture
async def song_one(sqlalchemy):
    song_create = {
        "title": "Song title 1",
        "is_active": True,
    }
    
    async with sqlalchemy() as session:
        song = await SongService(db=session).create(
            schema_in=SongCreate(**song_create)
        )
    return song
```

#### Pagination with dynamic filter and sorting in the service.

```python
import pytest
from tests.song.services import SongService


@pytest.mark.asyncio
async def test_song_service_with_or_and_asc_filter_paginate_song(sqlalchemy):
    criteria = [
        {"field": "foo", "op": "ilike", "value": "%bar%"},
    ]
    # Or with criteria in format or
    criteria = [
        {
            "or": [
                {"field": "title", "op": "==", "value": "Song title 2"},
                {"field": "title", "op": "==", "value": "Song title 3"},
            ]
        }
    ]
    sort = [
        {"field": "title", "direction": "asc"},
    ]
    async with sqlalchemy() as session:
        pagination = await SongService(db=session).paginate(
            page=1, per_page=5, criteria=criteria, sort=sort
        )
```

Operator options for filtering are:

`is_null, is_not_null, eq, ne, gt, lt, ge, le, like, ilike, not_ilike, in, not_in, any, not_any`

#### Use the create extended method on service

```python
import pytest
from tests.song.services import SongService
from tests.song.models import SongCreate


@pytest.mark.asyncio
async def test_song_service_create_song(sqlalchemy):
    song_data_one = {
        "title": "Song title 1",
        "is_active": True,
    }
    async with sqlalchemy() as session:
        song = await SongService(db=session).create(
            schema_in=SongCreate(**song_data_one)
        )
```

#### Update method on service

```python
import pytest
from tests.song.services import SongService
from tests.song.models import SongUpdate


@pytest.mark.asyncio
async def test_song_service_update_song(sqlalchemy, song_one):
    song_data = {
        "title": "Song title 2",
        "is_active": False,
    }
    async with sqlalchemy() as session:
        song = await SongService(db=session).update(
            instance=song_one, schema_in=SongUpdate(**song_data)
        )
```

#### Get method on service to get one register

```python
import pytest
from tests.song.services import SongService


@pytest.mark.asyncio
async def test_song_service_get_song(sqlalchemy, song_one):
    async with sqlalchemy() as session:
        song = await SongService(db=session).get(id=song_one.id)
```

#### Delete method on service

```python
import pytest
from tests.song.services import SongService


@pytest.mark.asyncio
async def test_song_service_delete_song(sqlalchemy, song_one):
    async with sqlalchemy() as session:
        await SongService(db=session).delete(id=song_one.id)
```

#### Count method on service

```python
import pytest
from tests.song.services import SongService


@pytest.mark.asyncio
async def test_song_service_count_song(sqlalchemy):
    async with sqlalchemy() as session:
        total = await SongService(db=session).count()
```

## With MongoDB

Create the model, as in the example [product/models.py](tests/product/models.py)

Create and extend of `BaseRepositoryMotor` in you repository, as in the example [product/repositories.py](tests/product/repositories.py)

Create and extend you service, as in the example [product/services.py](tests/product/services.py)

The following is an example with the connection session, but pass the session as needed.

```python
import pytest
from motor.motor_asyncio import AsyncIOMotorClient


# Get you connection session of Motor, example next, but make as you
@pytest.fixture()
async def motor():
    client = AsyncIOMotorClient(
        "localhost",
        maxPoolSize=10,
        minPoolSize=10,
        tz_aware=True,
    )
    await client.drop_database("testing")
    session = client.get_database("testing")
    yield session
```

The following is an example with register created.

```python
import pytest
from tests.product.models import ProductCreate
from tests.product.services import ProductService


@pytest.fixture
async def product_one(motor, product_data_one):
    product_data = {
        "title": "Product title 1",
        "is_active": True,
    }
    product = await ProductService(db=motor).create(
        schema_in=ProductCreate(**product_data)
    )
    return product
```

#### Pagination with dynamic filter and sorting in the service.

```python
import pytest
from tests.product.services import ProductService


@pytest.mark.asyncio
async def test_product_service_with_or_and_asc_filter_paginate_product(
    app, motor, product_data_one
):
    criteria = {"title": "Product title 1"}
    sort = [("title", -1)]

    pagination = await ProductService(db=motor).paginate(
        page=1, per_page=5, criteria=criteria, sort=sort
    )
```

#### Use the create extended method on service

```python
import pytest
from tests.product.models import ProductCreate
from tests.product.services import ProductService


@pytest.mark.asyncio
async def test_product_service_create_product(motor):
    product_data = {
        "title": "Product title 1",
        "is_active": True,
    }
    product = await ProductService(db=motor).create(
        schema_in=ProductCreate(**product_data)
    )
```

#### Update method on service

```python
import pytest
from tests.product.models import ProductUpdate
from tests.product.services import ProductService


@pytest.mark.asyncio
async def test_product_service_update_product(motor, product_one):
    product_data = {
        "title": "Product title 2",
        "is_active": False,
    }
    product = await ProductService(db=motor).update(
        instance=product_one, schema_in=ProductUpdate(**product_data)
    )
```

#### Get method on service to get one register

```python
import pytest
from tests.product.services import ProductService


@pytest.mark.asyncio
async def test_product_service_get_product(motor, product_one):
    product = await ProductService(db=motor).get(_id=product_one.id)
```

#### Delete method on service

```python
import pytest
from tests.product.services import ProductService


@pytest.mark.asyncio
async def test_product_service_delete_product(motor, product_one):
    await ProductService(db=motor).delete(_id=product_one.id)
```

#### Count method on service

```python
import pytest
from tests.product.services import ProductService


@pytest.mark.asyncio
async def test_product_service_count_product(motor):
    total = await ProductService(db=motor).count()
```

### Inherited base service layer with FastApi

You can create an inherited base service layer and add its methods, 
as in the example in FastApi with convenience methods for 404:

```python
from fastapi import HTTPException, status
from pydantic import BaseModel
from service_repository.services import BaseService as Base


class BaseService(Base):
    """Class representing the base service."""
    def __init__(self, db) -> None:
        self.db = db

    async def get_or_404(self, **kwargs):
        """Get one instance by filter or 404 if not exists."""
        instance = await self.get(**kwargs)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return instance

    async def update_or_404(self, schema_in: BaseModel, **kwargs):
        """Update instance or 404 if not exists."""
        instance = await self.get_or_404(**kwargs)
        instance = await self.update(instance=instance, schema_in=schema_in)
        return instance

    async def delete_or_404(self, **kwargs):
        """Delete one instance by filter or 404 if not exists."""
        await self.get_or_404(**kwargs)
        await self.delete(**kwargs)
```

### Inherited base service layer with Flask

You can create an inherited base service layer and add its methods, 
as in the example in Flask with convenience methods for 404:

```python
from flask import abort
from pydantic import BaseModel
from service_repository.services import BaseService as Base


class BaseService(Base):
    """Class representing the base service."""
    def __init__(self, db) -> None:
        self.db = db

    async def get_or_404(self, **kwargs):
        """Get one instance by filter or 404 if not exists."""
        instance = await self.get(**kwargs)
        if not instance:
            raise abort(404)
        return instance

    async def update_or_404(self, schema_in: BaseModel, **kwargs):
        """Update instance or 404 if not exists."""
        instance = await self.get_or_404(**kwargs)
        instance = await self.update(instance=instance, schema_in=schema_in)
        return instance

    async def delete_or_404(self, **kwargs):
        """Delete one instance by filter or 404 if not exists."""
        await self.get_or_404(**kwargs)
        await self.delete(**kwargs)
```

## Security

If you discover any security related issues, please email fndmiranda@gmail.com instead of using the issue tracker.

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.