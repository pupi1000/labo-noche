from __future__ import annotations

from collections.abc import Callable

from .config import Settings
from .graph import build_graph, safe_message_payload
from .mock_agent import run_mock

EventSink = Callable[[dict], None]


def run_agent(
    question: str, provider: str, emit: EventSink, settings: Settings | None = None
) -> str:
    s = settings or Settings()
    provider = provider.lower().strip()

    if provider == "mock":
        return run_mock(question, emit, s)

    from langchain_core.messages import HumanMessage

    graph = build_graph(provider, s)
    emit({"node": "input", "kind": "input", "message": question})
    seen = None
    final_answer = ""
    for state in graph.stream(
        {"messages": [HumanMessage(content=question)]},
        config={"recursion_limit": max(4, s.max_steps)},
        stream_mode="values",
    ):
        last = state["messages"][-1]
        payload = safe_message_payload(last)
        signature = repr(payload)
        if signature == seen:
            continue
        seen = signature
        mtype = payload.get("type")
        if payload.get("tool_calls"):
            emit({"node": "agent", "kind": "tool_decision", **payload})
        elif mtype == "tool":
            emit({"node": "tools", "kind": "tool_result", **payload})
        elif mtype in {"ai", "AIMessage"} and payload.get("content"):
            final_answer = payload["content"]
            emit({"node": "answer", "kind": "final", "message": final_answer})
        elif mtype not in {"human", "system"}:
            emit({"node": "agent", "kind": "state", **payload})

    if not final_answer:
        final_answer = "La ejecucion termino sin una respuesta textual final. Revise la traza."
    return final_answer
