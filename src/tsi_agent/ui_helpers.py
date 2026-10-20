from __future__ import annotations


def graphviz_source(active: str = "input") -> str:
    nodes = ["input", "agent", "tools", "answer"]
    labels = {
        "input": "Usuario",
        "agent": "Agent / LLM",
        "tools": "Tools",
        "answer": "Respuesta",
    }
    lines = ["digraph G {", "rankdir=TB;", "node [shape=box, style=rounded];"]
    for node in nodes:
        attrs = []
        if node == active:
            attrs.append("penwidth=3")
        attr = ", " + ", ".join(attrs) if attrs else ""
        lines.append(f'{node} [label="{labels[node]}"{attr}];')
    lines += [
        "input -> agent;",
        'agent -> tools [label=" tool call "];',
        'tools -> agent [label=" observacion "];',
        'agent -> answer [label=" final "];',
        "}",
    ]
    return "\n".join(lines)


def compact_event(event: dict) -> str:
    kind = event.get("kind", "event")
    elapsed = event.get("elapsed_ms")
    prefix = f"[{elapsed:7.1f} ms] " if isinstance(elapsed, (int, float)) else ""
    tool = event.get("tool") or event.get("tool_name")
    if tool:
        return prefix + f"{kind}: {tool}"
    if event.get("tool_calls"):
        names = ", ".join(x.get("name", "tool") for x in event["tool_calls"])
        return prefix + f"decision: {names}"
    msg = str(event.get("message") or event.get("content") or "")
    return prefix + f"{kind}: {msg[:120]}"
