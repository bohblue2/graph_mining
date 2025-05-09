# Backend

## How to install

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv self update
uv python install 3.12 
uv python pin 3.12
uv venv --python 3.12
uv sync
```

## How to setup

```bash
scrapy startproject crawler 
brew install --build-from-source alembic
alembic init crawler/alembic
```

## How to run

```bash
cd backend   
source .venv/bin/activate
PYTHONPATH=$(pwd)
uvicorn main:app --reload
```
