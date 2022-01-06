from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ProductBase(BaseModel):
    title: str = Field(default=None, min_length=1, max_length=64)
    is_active: Optional[bool] = True


class Product(ProductBase):
    id: Optional[PyObjectId] = Field(alias="_id")


class ProductCreate(ProductBase):
    title: str


class ProductUpdate(ProductBase):
    pass
