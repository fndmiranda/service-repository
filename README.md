# Service layer and repository for SQLAlchemy or MongoDB (asynchronous)

Simple service layer with repository to SQLAlchemy with SQLModel or MongoDB with Motor.

#### With SQLAlchemy

Create the model, as in the example [song/models.py](tests/song/models.py)

Create and extend of `BaseRepositorySqlalchemy` in you repository, as in the example [song/repositories.py](tests/song/repositories.py)

Create and extend you service, as in the example [song/services.py](tests/song/services.py)


#### With MongoDB

Create the model, as in the example [product/models.py](tests/product/models.py)

Create and extend of `BaseRepositoryMotor` in you repository, as in the example [product/repositories.py](tests/product/repositories.py)

Create and extend you service, as in the example [product/services.py](tests/product/services.py)

```python

```

### Pagination with dynamic filter and sorting.

Pass the `filter` field in query string, as in the example:



```python
from tests.song.services import SongService

criteria = [{"field": "foo", "op": "ilike", "value": "%bar%"}]

async with sqlalchemy() as session:
    pagination = await SongService(db=session).paginate(
        page=1, per_page=5, criteria=criteria, sort=sort
    )
```

or

```python
{
    "or": [
        {"field": "title", "op": "==", "value": "Song title 2"},
        {"field": "title", "op": "==", "value": "Song title 3"},
    ]
}
```

Operators options are:

`is_null, is_not_null, eq, ne, gt, lt, ge, le, like, ilike, not_ilike, in, not_in, any, not_any`

Pass the `sort` field in query string, as in the example:

```python
[{"field": "foo", "direction": "asc"}]
```
or
```python
[{"field": "foo", "direction": "desc"}]
```

### With MongDB

```python
from tests.product.services import ProductService
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(
    "localhost",
    maxPoolSize=10,
    minPoolSize=10,
    tz_aware=True,
)

criteria = {"title": "Product title 1"}
pagination = await ProductService(db=client).paginate(
    page=1, per_page=5, criteria=criteria
)
```