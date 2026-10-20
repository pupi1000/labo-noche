# Arquitectura del laboratorio

```mermaid
flowchart TD
    U[Usuario] --> A[Agent / LLM]
    A -->|tool call| T[Tool dispatcher]
    T --> D[Datos CSV]
    T --> K[Documentos locales]
    T --> C[Calculo]
    D --> A
    K --> A
    C --> A
    A -->|sin tool call| R[Respuesta]
    A -. trazas observables .-> O[UI / JSON logs]
```

Principio didactico: el modelo decide **que herramienta necesita**; las herramientas realizan operaciones verificables. La interfaz muestra acciones observables, no razonamiento privado del modelo.
