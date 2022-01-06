from service_layer.services import AbstractService
from tests.product.repositories import ProductRepository


class ProductService(AbstractService):
    """Class representing the product service."""

    _repository = ProductRepository
