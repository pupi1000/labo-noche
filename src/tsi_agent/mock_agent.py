from __future__ import annotations

import re

from .config import Settings
from .tool_registry import get_domain_tools
from .tools.data_tools import comparar_periodos, resumen_ventas
from .tools.document_tools import buscar_documentos


def _registered_tool(name: str, settings: Settings):
    for tool in get_domain_tools(settings.enable_student_extension):
        if tool.__name__ == name:
            return tool
    return None


def run_mock(question: str, emit, settings: Settings | None = None):
    s = settings or Settings()
    q = question.lower()
    emit({"node": "agent", "kind": "decision", "message": "Analizando la solicitud."})

    if "region" in q:
        extension = _registered_tool("comparar_regiones", s)
        if extension is None:
            answer = (
                "La comparacion regional es el reto de extension del estudiante. "
                "Implemente comparar_regiones(), registre la tool y active "
                "ENABLE_STUDENT_EXTENSION=true."
            )
            emit({"node": "answer", "kind": "final", "message": answer})
            return answer

        product = "Killa"
        for candidate in ["Altiplano", "Killa", "Illimani", "Tunari"]:
            if candidate.lower() in q:
                product = candidate
        period = "Q3"
        match = re.search(r"q[1-4]", q)
        if match:
            period = match.group(0).upper()
        emit(
            {
                "node": "tools",
                "kind": "tool_start",
                "tool": "comparar_regiones",
                "args": {"producto": product, "periodo": period},
            }
        )
        result = extension(product, period)
        emit(
            {
                "node": "tools",
                "kind": "tool_result",
                "tool": "comparar_regiones",
                "result": result,
            }
        )
        leader = result["region_lider"]
        answer = (
            f"Para {product} en {period}, la region lider es {leader['region']} "
            f"con ingresos {leader['ingresos']:.2f}."
        )
        emit({"node": "answer", "kind": "final", "message": answer})
        return answer

    if any(x in q for x in ["crecimiento", "incremento", "q2", "q3"]):
        emit(
            {
                "node": "tools",
                "kind": "tool_start",
                "tool": "comparar_periodos",
                "args": {
                    "periodo_inicial": "Q2",
                    "periodo_final": "Q3",
                    "agrupacion": "producto",
                },
            }
        )
        comp = comparar_periodos("Q2", "Q3", "producto")
        emit(
            {
                "node": "tools",
                "kind": "tool_result",
                "tool": "comparar_periodos",
                "result": comp,
            }
        )
        top = comp["mayor_crecimiento"]
        name = top["producto"]
        emit(
            {
                "node": "agent",
                "kind": "decision",
                "message": "Necesito evidencia documental para explicar el cambio.",
            }
        )
        query = f"{name} Q3 promocion campana cambio"
        emit(
            {
                "node": "tools",
                "kind": "tool_start",
                "tool": "buscar_documentos",
                "args": {"consulta": query},
            }
        )
        docs = buscar_documentos(query)
        emit(
            {
                "node": "tools",
                "kind": "tool_result",
                "tool": "buscar_documentos",
                "result": docs,
            }
        )
        sources = [item["fuente"] for item in docs["resultados"] if not item["marcador_inyeccion"]]
        evidence = ", ".join(sources[:2]) or "sin documentos relevantes"
        answer = (
            f"El mayor crecimiento de ingresos entre Q2 y Q3 corresponde a {name}: "
            f"{top['variacion_pct']}%. Como evidencia contextual aparecen {evidence}. "
            "Los documentos se trataron como datos no confiables y no como instrucciones."
        )
        emit({"node": "answer", "kind": "final", "message": answer})
        return answer

    if "document" in q or "killa" in q or "promoc" in q:
        emit(
            {
                "node": "tools",
                "kind": "tool_start",
                "tool": "buscar_documentos",
                "args": {"consulta": question},
            }
        )
        docs = buscar_documentos(question)
        emit(
            {
                "node": "tools",
                "kind": "tool_result",
                "tool": "buscar_documentos",
                "result": docs,
            }
        )
        sources = [item["fuente"] for item in docs["resultados"]]
        answer = "Documentos encontrados: " + ", ".join(sources)
        emit({"node": "answer", "kind": "final", "message": answer})
        return answer

    emit(
        {
            "node": "tools",
            "kind": "tool_start",
            "tool": "resumen_ventas",
            "args": {"periodo": "Q3", "agrupacion": "producto"},
        }
    )
    summary = resumen_ventas("Q3", "producto")
    emit(
        {
            "node": "tools",
            "kind": "tool_result",
            "tool": "resumen_ventas",
            "result": summary,
        }
    )
    leader = summary["filas"][0]
    answer = f"En Q3, {leader['producto']} lidera ingresos con {leader['ingresos']:.2f}."
    emit({"node": "answer", "kind": "final", "message": answer})
    return answer
