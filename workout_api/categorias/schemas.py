from typing import Annotated
from pydantic import UUID4, Field, ConfigDict
from workout_api.contrib.schemas import BaseSchema, OutMixin
from datetime import datetime

class Categoria(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example="Iniciante", max_length=10)]

class CategoriaIn(Categoria):
    pass

class CategoriaOut(CategoriaIn, OutMixin):
    id: Annotated[UUID4, Field(description='ID da categoria', example=1)]
    created_at: Annotated[datetime, Field(description='Data de criação')]

    model_config = ConfigDict(from_attributes=True)