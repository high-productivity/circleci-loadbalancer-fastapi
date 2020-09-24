from datetime import datetime
# from typing import Optional

# from pydantic import BaseModel

from pydantic import BaseModel, Schema, validator
from fastapi.encoders import jsonable_encoder
from typing import Optional, Any
from bson import ObjectId


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] # = Schema(..., alias="createdAt")
    updated_at: Optional[datetime] # = Schema(..., alias="updatedAt")


class DBModelMixin(DateTimeModelMixin):
    id: Optional[int] = None


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(str(v)):
            return ValueError(f"Not a valid ObjectId: {v}")
        return ObjectId(str(v))

class DBModelMixin2(BaseModel):
    id: Optional[ObjectIdStr] = Schema(..., alias="_id")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: lambda x: str(x)}
