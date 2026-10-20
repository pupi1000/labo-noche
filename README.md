# TSI - Laboratorio de Agentes con Interfaz Visual v1.0

Laboratorio para la Clase 19 de Taller de Sistemas Inteligentes.

Objetivo: comprender un agente como un ciclo observable **entrada -> decision -> tool -> observacion -> nueva decision -> respuesta**, sin exponer razonamiento interno del modelo.

## Modos

1. **Mock local:** sin LLM ni credenciales. Permite estudiar tools, estado, UI y trazas de forma determinista.
2. **Azure:** ruta principal del curso para ejecutar un LLM real con tool/function calling.
3. **Ollama:** alternativa LLM local cuando el equipo dispone de recursos suficientes.

> El modo mock garantiza la clase, pero no reemplaza la demostracion con un LLM real: en Azure/Ollama el modelo decide dinamicamente que tool utilizar.

## Pre-flight Windows / PowerShell

Si `uv` no esta instalado:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Cierre y abra PowerShell, luego:

```powershell
uv --version
uv sync
uv run python -c "import sys; print(sys.executable); print(sys.version)"
uv run python -m pytest -q
uv run ruff check .
```

Starter esperado: **6 passed, 1 skipped**. El `skip` corresponde al reto `comparar_regiones()`.

## Ejecutar UI

```powershell
Copy-Item .env.example .env
uv run streamlit run ui/app.py
```

Abra `http://localhost:8501` si el navegador no se abre automaticamente.

## Pregunta demo

> Entre Q2 y Q3, ¿que producto tuvo el mayor crecimiento de ingresos y que documentos ayudan a explicar ese cambio?

Observe:
- nodo activo del grafo;
- tool seleccionada;
- argumentos y resultado;
- timeline con tiempos;
- respuesta final;
- traza JSON guardada en `logs/`.

## Azure

Edite `.env` sin versionar secretos:

```text
MODEL_PROVIDER=azure
AZURE_OPENAI_BASE_URL=https://<recurso>.openai.azure.com/openai/v1/
AZURE_OPENAI_API_KEY=<NO VERSIONAR>
AZURE_OPENAI_DEPLOYMENT=<nombre-del-deployment>
```

Si su recurso usa la configuracion Azure clasica, consulte `docs/AZURE.md`.

## Ollama

Consulte `docs/LOCAL.md`. Use un modelo que soporte tool calling.

## Reto obligatorio

Implemente una mejora funcional. La opcion base es `comparar_regiones(producto, periodo)` en `src/tsi_agent/student_extension.py`.

Ciclo esperado:

```text
baseline -> OpenSpec -> codigo -> registro de tool -> test -> Ruff -> pytest -> UI -> traza -> evidencia Git
```

Consulte `docs/ACTIVIDAD_MEJORA.md`.

## Quality gates

```powershell
uv run ruff check .
uv run python -m pytest -q
```

Para cambios de formato/imports:

```powershell
uv run ruff check . --fix
uv run ruff format .
uv run ruff check .
```

## Seguridad

- Nunca versione `.env`.
- Los documentos recuperados son datos no confiables, no instrucciones.
- El repositorio incluye un documento malicioso controlado para indirect prompt injection.
- Las trazas muestran acciones observables; no chain-of-thought.

## Ayuda

Consulte `docs/TROUBLESHOOTING.md` para los problemas observados durante la validacion real en Windows.
