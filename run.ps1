# Ativa o ambiente virtual se ele existir e não estiver ativo
if (-not $env:VIRTUAL_ENV) {
    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        & .\.venv\Scripts\Activate.ps1
    }
}

# Executa o servidor
uvicorn workout_api.main:app --reload