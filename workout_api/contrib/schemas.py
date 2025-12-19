from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.types import UUID4
from typing import Annotated

class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True

class OutMixin(BaseModel):
    id: Annotated[UUID4, Field(description='Identificador único')]
    created_at: Annotated[datetime, Field(description='Data de criação')]