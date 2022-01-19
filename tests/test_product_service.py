import pytest

from tests.product.models import ProductCreate, ProductUpdate
from tests.product.services import ProductService


@pytest.mark.asyncio
async def test_product_service_create_product(app, motor, product_data_one):
    product = await ProductService(db=motor).create(
        schema_in=ProductCreate(**product_data_one)
    )

    assert getattr(product, "id") is not None
    for key, value in product_data_one.items():
        assert getattr(product, key) == product_data_one[key]


@pytest.mark.asyncio
async def test_product_service_update_product(
    app, motor, product_one, product_data_two
):
    product = await ProductService(db=motor).update(
        instance=product_one, schema_in=ProductUpdate(**product_data_two)
    )
    assert product_one.id == product.id
    for key, value in product_data_two.items():
        assert getattr(product, key) == product_data_two[key]


@pytest.mark.asyncio
async def test_product_service_get_product(app, motor, product_one):
    product = await ProductService(db=motor).get(_id=product_one.id)
    assert product is not None


@pytest.mark.asyncio
async def test_product_service_paginate_product(app, motor, product_data_one):
    count = 15
    for item in range(count):
        product_data_one.update(
            {
                "title": f"Product title {item}",
            }
        )

        await ProductService(db=motor).create(
            schema_in=ProductCreate(**product_data_one)
        )

    pagination = await ProductService(db=motor).paginate(page=1, per_page=5)

    assert pagination["per_page"] == 5
    assert len(pagination["items"]) == 5
    assert pagination["num_pages"] == 3
    assert pagination["page"] == 1
    assert pagination["total"] == 15


@pytest.mark.asyncio
async def test_product_service_with_filter_paginate_product(
    app, motor, product_data_one
):
    count = 5
    criteria = {"title": "Product title 1"}

    for item in range(count):
        product_data_one.update(
            {
                "title": f"Product title {item}",
            }
        )

        await ProductService(db=motor).create(
            schema_in=ProductCreate(**product_data_one)
        )

    pagination = await ProductService(db=motor).paginate(
        page=1, per_page=5, criteria=criteria
    )

    assert len(pagination["items"]) == 1
    assert pagination["total"] == 1


@pytest.mark.asyncio
async def test_product_service_with_or_and_asc_filter_paginate_product(
    app, motor, product_data_one
):
    count = 5
    criteria = {"title": "Product title 1"}

    for item in range(count):
        product_data_one.update(
            {
                "title": f"Product title {item}",
            }
        )

        await ProductService(db=motor).create(
            schema_in=ProductCreate(**product_data_one)
        )

    pagination = await ProductService(db=motor).paginate(
        page=1, per_page=5, criteria=criteria
    )

    assert len(pagination["items"]) == 1
    assert pagination["total"] == 1


@pytest.mark.asyncio
async def test_product_service_with_sort_desc_paginate_product(
    app, motor, product_data_one
):
    count = 5
    sort = [("title", -1)]

    for item in range(count):
        product_data_one.update(
            {
                "title": f"Product title {item}",
            }
        )

        await ProductService(db=motor).create(
            schema_in=ProductCreate(**product_data_one)
        )

    pagination = await ProductService(db=motor).paginate(
        page=1, per_page=5, sort=sort
    )

    assert pagination["items"][0].title == "Product title 4"


@pytest.mark.asyncio
async def test_product_service_delete_product(app, motor, product_one):
    await ProductService(db=motor).delete(_id=product_one.id)
    product = await ProductService(db=motor).get(_id=product_one.id)
    assert product is None


@pytest.mark.asyncio
async def test_product_service_count_product(app, motor, product_data_one):
    count = 10
    for item in range(count):
        product_data_one.update(
            {
                "title": f"Product title {item}",
            }
        )

        await ProductService(db=motor).create(
            schema_in=ProductCreate(**product_data_one)
        )

    total = await ProductService(db=motor).count()

    assert total == count
