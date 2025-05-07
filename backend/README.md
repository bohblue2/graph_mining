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

## How to run

```bash
uvicorn main:app --reload
```
