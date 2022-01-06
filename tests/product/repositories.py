from service_layer.repositories.motor import AbstractRepositoryMotor
from tests.product.models import Product


class ProductRepository(AbstractRepositoryMotor):
    """Class representing the product repository."""

    _model = Product
    _collection = "product"
