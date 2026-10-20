# Ejecucion local

## 1. Mock local - recomendado para el primer recorrido

```text
MODEL_PROVIDER=mock
```

No usa un LLM. Ejecuta un flujo determinista con las mismas tools de dominio y genera eventos observables. Sirve para estudiar arquitectura, UI, trazas y fallbacks sin depender de red o credenciales.

> Mock no demuestra seleccion probabilistica de tools por un LLM. Esa comparacion se realiza luego con Azure u Ollama.

## 2. Ollama local - LLM real

Instale Ollama y un modelo que soporte tool calling. Ejemplo de flujo:

```powershell
ollama pull llama3.1:8b
ollama serve
```

`.env`:

```text
MODEL_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

Puede sustituir el modelo por otro instalado compatible con tools. Si el equipo no tiene RAM/VRAM suficiente, use mock o Azure.

## Verificacion

```powershell
uv run streamlit run ui/app.py
```

Seleccione `ollama` en la barra lateral y repita la misma pregunta usada en mock. Compare la secuencia de tools y la respuesta.
