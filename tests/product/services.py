from service_repository.services import ServiceLayer
from tests.product.repositories import ProductRepository


class ProductService(ServiceLayer):
    """Class representing the product service."""

    _repository = ProductRepository
