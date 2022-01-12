from service_repository.repositories.motor import RepositoryMotor
from tests.product.models import Product


class ProductRepository(RepositoryMotor):
    """Class representing the product repository."""

    _model = Product
    _collection = "product"
