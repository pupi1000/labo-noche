from tsi_agent.tools.data_tools import calcular_variacion, comparar_periodos, resumen_ventas


def test_resumen_q3_tiene_productos():
    result = resumen_ventas("Q3", "producto")
    assert len(result["filas"]) == 4
    assert result["filas"][0]["ingresos"] > 0


def test_comparar_periodos_identifica_crecimiento():
    result = comparar_periodos("Q2", "Q3", "producto")
    top = result["mayor_crecimiento"]
    assert top["producto"] == "Killa"
    assert top["variacion_pct"] > 20


def test_calcular_variacion():
    result = calcular_variacion(100, 125)
    assert result["variacion_pct"] == 25.0
