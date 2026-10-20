from __future__ import annotations

import time
from pathlib import Path

import pandas as pd
import streamlit as st

from tsi_agent.config import Settings, provider_readiness
from tsi_agent.runner import run_agent
from tsi_agent.trace import save_trace
from tsi_agent.ui_helpers import compact_event, graphviz_source

ROOT = Path(__file__).resolve().parents[1]

st.set_page_config(page_title="TSI Agent Lab", page_icon="🧭", layout="wide")
st.title("Laboratorio TSI - Agente con tools y trazas")
st.caption(
    "Visualice acciones observables del agente: decisiones de tool, argumentos, resultados y respuesta final."
)

settings = Settings()
provider = st.sidebar.selectbox(
    "Proveedor",
    ["mock", "azure", "ollama"],
    index=["mock", "azure", "ollama"].index(settings.provider)
    if settings.provider in {"mock", "azure", "ollama"}
    else 0,
)
ready, readiness = provider_readiness(provider, settings)
(st.sidebar.success if ready else st.sidebar.warning)(readiness)
st.sidebar.markdown("**Regla:** nunca mostrar ni versionar secretos.")
st.sidebar.caption("Mock = flujo determinista; Azure/Ollama = LLM con tool calling.")

if "chat" not in st.session_state:
    st.session_state.chat = []
if "events" not in st.session_state:
    st.session_state.events = []
if "active_node" not in st.session_state:
    st.session_state.active_node = "input"

left, right = st.columns([1.25, 1])

with right:
    st.subheader("Grafo de ejecucion")
    graph_ph = st.empty()
    graph_ph.graphviz_chart(graphviz_source(st.session_state.active_node), width="stretch")
    st.subheader("Timeline observable")
    timeline_ph = st.empty()
    if st.session_state.events:
        timeline_ph.code(
            "\n".join(
                f"{i + 1:02d}. {compact_event(e)}" for i, e in enumerate(st.session_state.events)
            ),
            language="text",
        )
    else:
        timeline_ph.info("Ejecute una consulta para generar eventos.")

with left:
    st.subheader("Conversacion")
    for role, text in st.session_state.chat:
        with st.chat_message(role):
            st.markdown(text)

question = st.chat_input("Pregunte por ventas, crecimiento, documentos o regiones...")
if question:
    st.session_state.chat.append(("user", question))
    st.session_state.events = []
    with left:
        with st.chat_message("user"):
            st.markdown(question)
        answer_box = st.chat_message("assistant")
        status = st.status("Ejecutando agente...", expanded=True)

    start_run = time.perf_counter()

    def emit(event: dict):
        event = dict(event)
        event["elapsed_ms"] = round((time.perf_counter() - start_run) * 1000, 1)
        st.session_state.events.append(event)
        node = event.get("node", "agent")
        st.session_state.active_node = node
        graph_ph.graphviz_chart(graphviz_source(node), width="stretch")
        timeline_ph.code(
            "\n".join(
                f"{i + 1:02d}. {compact_event(e)}" for i, e in enumerate(st.session_state.events)
            ),
            language="text",
        )
        if event.get("tool"):
            status.write(f"Tool: {event['tool']}")
        elif event.get("tool_calls"):
            status.write("Decision de tool registrada")
        elif event.get("message") and event.get("kind") != "final":
            status.write(str(event["message"])[:180])

    if not ready:
        answer = f"Proveedor no listo: {readiness} Cambie a mock o complete la configuracion."
        emit({"node": "answer", "kind": "final", "message": answer})
    else:
        try:
            answer = run_agent(question, provider, emit, settings)
        except Exception as exc:
            answer = f"Error controlado al ejecutar {provider}: {type(exc).__name__}: {exc}"
            emit({"node": "answer", "kind": "error", "message": answer})

    trace_path = save_trace(question, provider, st.session_state.events, answer)
    with left:
        answer_box.markdown(answer)
        status.update(label="Ejecucion finalizada", state="complete")
        st.caption(f"Traza: {trace_path.relative_to(ROOT)}")
    st.session_state.chat.append(("assistant", answer))

st.divider()
tab1, tab2, tab3 = st.tabs(["Datos", "Ultima traza", "Seguridad"])
with tab1:
    df = pd.read_csv(ROOT / "data" / "ventas.csv")
    st.dataframe(df.head(30), width="stretch")
with tab2:
    if st.session_state.events:
        st.json(st.session_state.events, expanded=False)
    else:
        st.info("Aun no hay una traza en esta sesion.")
with tab3:
    st.markdown(
        "Los documentos recuperados se consideran **datos no confiables**. El agente no debe ejecutar instrucciones contenidas dentro de ellos. "
        "El laboratorio incluye un documento malicioso controlado para probar esta regla."
    )
