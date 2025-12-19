# 🏋️ WorkoutAPI — Sistema de Gerenciamento de Atletas

API para gerenciamento de atletas de competições de CrossFit, desenvolvida com **FastAPI** e programação assíncrona (async).

Projeto baseado no repositório oficial da **Digital Innovation One (DIO)**:  
https://github.com/digitalinnovationone/workout_api

Este projeto foi desenvolvido após assistir às aulas, com foco em aprendizado prático e melhorias na arquitetura, incluindo o uso de **Poetry** e **Alembic**.

<img width="2395" height="516" alt="image" src="https://github.com/user-attachments/assets/67733b04-dbd2-4479-9b83-abbe4f49dc39" />

---

## 🚀 Tecnologias Utilizadas

- Python 3.11+
- FastAPI
- Async / Await
- Pydantic
- SQLAlchemy
- Poetry
- Alembic
- Uvicorn
- Banco de Dados Relacional

---

## 📦 Gerenciamento de Dependências (Poetry)

O projeto utiliza o **Poetry** para gerenciamento de dependências e ambientes virtuais.

### Instalar o Poetry
```bash
pip install poetry
```

### Instalar dependências do projeto
```bash
poetry install
```

### Ativar o ambiente virtual
```bash
poetry shell
```

### Executar a aplicação
```bash
poetry run uvicorn workout_api.main:app --reload
```

---

## 🗄️ Migrações de Banco de Dados (Alembic)

O **Alembic** é utilizado para versionar e gerenciar as migrações do banco de dados.

### Criar uma nova migração
```bash
alembic revision --autogenerate -m "descrição da migração"
```

### Aplicar migrações
```bash
alembic upgrade head
```

### Reverter migração
```bash
alembic downgrade -1
```

---

## 📄 Documentação da API

A documentação interativa é gerada automaticamente pelo FastAPI:

- **Swagger UI**: `/docs`
- **Redoc**: `/redoc`

---

## 📌 Melhorias Implementadas

- Documentação clara dos endpoints
- Paginação na listagem de atletas
- Filtros por nome e CPF
- Tratamento de erro para CPF duplicado
- Respostas otimizadas
- Gerenciamento de dependências com Poetry
- Migrações de banco de dados com Alembic

---

## 🔗 Endpoints Principais

### Listar Atletas

**`GET /atletas`**

**Parâmetros de query (opcionais):**

| Parâmetro | Descrição |
|-----------|-----------|
| `nome` | Filtra pelo nome do atleta |
| `cpf` | Filtra pelo CPF |
| `limit` | Quantidade de registros por página |
| `offset` | Ponto inicial da paginação |

**Exemplo de resposta:**
```json
[
  {
    "nome": "João Silva",
    "centro_treinamento": "CT Força Total",
    "categoria": "Pro"
  }
]
```

<img width="783" height="122" alt="image" src="https://github.com/user-attachments/assets/5b660d8f-5b1b-47b7-94c6-a176e40a6e03" />


### Criar Atleta

**`POST /atletas`**

Caso tente cadastrar um CPF já existente, a API retornará:

**Status:** `409 Conflict`
```json
{
  "detail": "O CPF 12345678900 já está cadastrado para outro atleta."
}
```

---
<img width="599" height="216" alt="image" src="https://github.com/user-attachments/assets/0faec199-5246-4dcc-8fa4-7b95baae9134" />

## 📁 Estrutura do Projeto
```
workout_api/
├── atleta/
├── categorias/
├── centro_treinamento/
├── configs/
├── alembic/
├── pyproject.toml
└── main.py
```

---

## 🎯 Objetivo do Projeto

Projeto desenvolvido com foco em:

- Arquitetura de APIs REST
- Boas práticas com FastAPI
- Programação assíncrona
- Organização modular
- Versionamento de banco de dados
- Gerenciamento de dependências com Poetry

---

## 🤝 Créditos

**Projeto base:** Digital Innovation One (DIO)  
**Implementação e melhorias:** Marcos Antônio de Aguiar Júnior
