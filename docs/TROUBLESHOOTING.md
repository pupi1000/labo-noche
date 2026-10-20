# Troubleshooting validado - Windows / PowerShell

## `uv` no se reconoce

Instale `uv`, cierre la terminal y abra una nueva:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version
```

## Warning `Failed to hardlink files`

No es un error. `uv` continuara copiando archivos. Para silenciarlo en PowerShell:

```powershell
$env:UV_LINK_MODE="copy"
uv sync
```

Tambien puede usar `uv sync --link-mode=copy`.

## `ModuleNotFoundError: No module named 'tsi_agent'`

Compruebe que ejecuta el Python del entorno de `uv`:

```powershell
uv run python -c "import sys; print(sys.executable); print(sys.version)"
uv run python -m pytest -q
```

Evite invocar un `pytest` global de otra version de Python.

## Ruff muestra `I001`

```powershell
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
```

El paquete v1.0 ya se entrega con Ruff limpio; esta receta sirve para cambios del estudiante.

## Streamlit muestra advertencia sobre `use_container_width`

La v1.0 usa `width="stretch"`. Si esta usando una copia anterior, reemplace `use_container_width=True` por `width="stretch"` en `ui/app.py`.

## Streamlit muestra `Help agents write better apps`

Es un aviso propio de Streamlit. No forma parte del laboratorio. Puede cerrarlo o elegir `Don't show again`.

## Puerto 8501 ocupado

```powershell
uv run streamlit run ui/app.py --server.port 8502
```

## Azure no esta listo

Vuelva temporalmente a `mock`. Revise `.env`, deployment, endpoint/base URL y credencial. No copie secretos en commits o capturas.

## El modelo no llama tools

Use un deployment/modelo con soporte de tool/function calling. Repita una pregunta que requiera datos verificables y revise la traza.

## Ollama no conecta

Compruebe servicio, modelo y puerto:

```powershell
ollama list
ollama serve
```

Si el equipo no tiene recursos suficientes, use `mock` o Azure.
