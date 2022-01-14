from service_repository.repositories.motor import BaseRepositoryMotor
from tests.product.models import Product


class ProductRepository(BaseRepositoryMotor):
    """Class representing the product repository."""

    class Config:
        model = Product
        collection = "product"
