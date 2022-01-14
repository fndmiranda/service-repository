from service_repository.services import BaseService
from tests.product.repositories import ProductRepository


class ProductService(BaseService):
    """Class representing the product service."""

    class Config:
        repository = ProductRepository
