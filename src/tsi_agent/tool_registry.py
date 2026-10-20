from __future__ import annotations

from .tools.data_tools import calcular_variacion, comparar_periodos, resumen_ventas
from .tools.document_tools import buscar_documentos


def get_domain_tools(enable_student_extension: bool = False):
    tools = [resumen_ventas, comparar_periodos, calcular_variacion, buscar_documentos]
    if enable_student_extension:
        from .student_extension import comparar_regiones

        tools.append(comparar_regiones)
    return tools
