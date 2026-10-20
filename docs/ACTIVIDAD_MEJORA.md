# Actividad obligatoria - Mejorar el agente

## Objetivo

Demostrar que comprende la diferencia entre **usar** un agente y **extender** un agente con nueva capacidad verificable.

## Baseline antes de modificar

Ejecute:

```powershell
uv run python -m pytest -q
uv run ruff check .
uv run streamlit run ui/app.py
```

En el starter debe obtener **6 passed, 1 skipped**. Luego pregunte:

> Compara el desempeno regional de Killa en Q3.

El agente debe indicar que esa capacidad aun no esta implementada.

## Ciclo profesional obligatorio

1. Complete `openspec/agent-improvement.md`.
2. Implemente `comparar_regiones(producto, periodo)` en `src/tsi_agent/student_extension.py`.
3. Registre la tool en `src/tsi_agent/tool_registry.py`.
4. Cambie `ENABLE_STUDENT_EXTENSION=true` en `.env`.
5. Habilite y complete `tests/test_student_extension.py`.
6. Ejecute `uv run ruff check . --fix` si hace falta y luego `uv run ruff format .`.
7. Ejecute `uv run ruff check .` y `uv run python -m pytest -q`.
8. Ejecute la consulta regional desde la UI.
9. Muestre en el timeline `comparar_regiones`, argumentos y resultado.
10. Entregue commit/PR y la traza JSON.

## Contrato minimo de la tool

```python
comparar_regiones(producto: str, periodo: str = "Q3") -> dict
```

Debe devolver como minimo:
- ingresos por region;
- region con mayores ingresos;
- diferencia porcentual entre la primera y la segunda region;
- filas de evidencia.

## Mejora alternativa

Con autorizacion docente puede reemplazar la mejora base por una de complejidad equivalente:
- deteccion de anomalias;
- approval gate antes de una accion sensible;
- busqueda documental con embeddings;
- memoria de sesion limitada y verificable;
- fallback Azure -> Ollama/mock;
- metricas adicionales de ejecucion.

Una mejora solo cosmetica de UI no reemplaza una mejora funcional.

## Evidencia

- spec breve completa;
- codigo funcional;
- al menos una prueba;
- Ruff y pytest verdes;
- ejecucion en interfaz;
- timeline/traza con la nueva capacidad;
- commit o PR;
- explicacion de 2 minutos: problema, cambio, prueba y resultado.

## Pregunta de defensa

¿Por que esta mejora necesita una tool o un cambio del flujo del agente, y no solamente una instruccion adicional en el prompt?
