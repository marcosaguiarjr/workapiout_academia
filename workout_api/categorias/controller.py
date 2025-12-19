from pydantic import UUID4
from fastapi import APIRouter, status, Body, HTTPException
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.categorias.models import CategoriaModel
from sqlalchemy.future import select

router = APIRouter()

@router.post("/", summary="Criar nova categoria", status_code=status.HTTP_201_CREATED, response_model=CategoriaOut)
async def post(
    db_session: DatabaseDependency, 
    categoria_in: CategoriaIn
) -> CategoriaOut:
    # 1. Transforma o Schema em Modelo do SQLAlchemy
    categoria_model = CategoriaModel(**categoria_in.model_dump())
    
    # 2. Adiciona e salva no banco
    db_session.add(categoria_model)
    await db_session.commit()
    
    # 3. O SEGREDO: Refresh busca os campos gerados pelo banco (id, created_at)
    await db_session.refresh(categoria_model)

    # 4. Retorna o modelo (o FastAPI cuidará de converter para CategoriaOut)
    return categoria_model


@router.get("/", summary="Consultar todas as categorias", 
             status_code=status.HTTP_200_OK,
             response_model=list[CategoriaOut])

async def query(
    db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return categorias

@router.get(
    '/{id}', 
    summary='Consulta uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )
    
    return categoria