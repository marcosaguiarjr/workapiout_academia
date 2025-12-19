from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select
from fastapi_pagination import Page, paginate

from typing import Optional

router = APIRouter()

@router.get(
    '/ConsultaAtletaNomeCPF', 
    summary='Consulta um Atleta pelo nome e/ou cpf',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(db_session: DatabaseDependency, 
              nome: Optional[str] = None,
              cpf: Optional[str] = None) -> AtletaOut:
    # Criamos a base da query
    query = select(AtletaModel)

    # Adicionamos os filtros apenas se eles forem enviados
    if nome:
        query = query.filter(AtletaModel.nome == nome)
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    result = await db_session.execute(query)
    atleta = result.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Atleta não encontrado com os critérios fornecidos.'
        )
    
    return atleta

@router.get(
    '/ConsultaAtletaComPaginacao', 
    summary='Consultar todos os Atletas com paginacao',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaOut],
)
async def query(db_session: DatabaseDependency):
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    
    return paginate(atletas)

@router.post(
    '/', 
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)
):   
    # 1. Busca as dependências (Categoria e CT)
    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(status_code=400, detail=f'A categoria {atleta_in.categoria.nome} não encontrada.')
    
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))
    ).scalars().first()

    atleta_cpf = (await db_session.execute(
        select(AtletaModel).filter_by(cpf=atleta_in.cpf))
    ).scalars().first()

    if atleta_cpf:
        raise HTTPException(status_code=400, detail=f'O CPF {atleta_in.cpf} já está cadastrado para outro atleta.')
    
    if not centro_treinamento:
        raise HTTPException(status_code=400, detail=f'O CT {atleta_in.centro_treinamento.nome} não encontrado.')

    try:
        # 2. Cria o modelo excluindo campos de schema que não são do banco
        atleta_model = AtletaModel(**atleta_in.model_dump(exclude={'categoria', 'centro_treinamento'}))
        
        # 3. Atribui as chaves estrangeiras e gera os IDs
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        atleta_model.id = uuid4()  # Atribui o UUID manualmente se não for default no model
        atleta_model.created_at = datetime.utcnow()

        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model) # Recupera o objeto completo do banco

        return atleta_model # O FastAPI converte para AtletaOut automaticamente

    except Exception as e:
        # Dica: Durante o desenvolvimento, imprima o erro real no console
        print(f"ERRO DE BANCO: {e}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

@router.get(
    '/', 
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    
    return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.get(
    '/{id}', 
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    return atleta

@router.patch(
    '/{id}', 
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta

@router.delete(
    '/{id}', 
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    await db_session.delete(atleta)
    await db_session.commit()