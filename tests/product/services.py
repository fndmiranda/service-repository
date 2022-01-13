from service_repository.services import BaseService
from tests.product.repositories import ProductRepository


class ProductService(BaseService):
    """Class representing the product service."""

    _repository = ProductRepository
