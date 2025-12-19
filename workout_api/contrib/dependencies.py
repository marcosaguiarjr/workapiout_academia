from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
# Importação explícita
from workout_api.configs.database import get_session

# A definição da dependência vem DEPOIS do import
DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]