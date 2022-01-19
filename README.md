# Service layer and repository for SQLAlchemy or MongoDB (asynchronous)

Simple service layer with repository to SQLAlchemy with SQLModel or MongoDB with Motor.

### Pagination with dynamic filter and sorting.

Pass the `filter` field in query string, as in the example:


#### With SQLAlchemy

```python
[{"field": "foo", "op": "ilike", "value": "%bar%"}]
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
