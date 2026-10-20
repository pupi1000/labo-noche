# Configuracion Azure

Azure es la ruta principal del laboratorio para demostrar un agente con LLM real.

## Opcion A - endpoint OpenAI v1

En `.env`:

```text
MODEL_PROVIDER=azure
AZURE_OPENAI_BASE_URL=https://<recurso>.openai.azure.com/openai/v1/
AZURE_OPENAI_API_KEY=<secreto>
AZURE_OPENAI_DEPLOYMENT=<deployment>
```

El deployment debe corresponder a un modelo disponible en su recurso y con soporte de tool/function calling.

## Opcion B - AzureChatOpenAI clasico

```text
MODEL_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://<recurso>.openai.azure.com/
OPENAI_API_VERSION=<version habilitada por su recurso>
AZURE_OPENAI_API_KEY=<secreto>
AZURE_OPENAI_DEPLOYMENT=<deployment>
```

## Prueba

1. Inicie la UI en modo mock y ejecute la pregunta base.
2. Cambie a `azure`.
3. Repita exactamente la misma pregunta.
4. Compare tool selection, cantidad de pasos, latencia y redaccion final.
5. Verifique que las cifras provengan de tools y no sean inventadas por el modelo.

## Seguridad

- `.env` esta ignorado por Git.
- No pegue la API key en README, CLAUDE.md, issues, commits ni capturas.
- Si una key se expone, rote/revoque la credencial.
- Para escenarios avanzados puede sustituirse la key por mecanismos de identidad administrada/Entra cuando la infraestructura lo permita.
