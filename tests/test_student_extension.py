import pytest

from tsi_agent.config import Settings
from tsi_agent.mock_agent import run_mock
from tsi_agent.student_extension import comparar_regiones


def test_extension_comparar_regiones():
    result = comparar_regiones("Killa", "Q3")
    assert result["region_lider"]["region"] in {"La Paz", "Cochabamba", "Santa Cruz"}
    assert result["region_lider"]["region"] == "La Paz"
    assert len(result["filas"]) == 3
    assert result["diferencia_pct_lider_vs_segundo"] > 0
    assert "La Paz" in result["ingresos_por_region"]


def test_extension_comparar_regiones_producto_invalido():
    with pytest.raises(ValueError, match="No existen datos"):
        comparar_regiones("ProductoFantasma", "Q3")


def test_mock_agent_con_comparar_regiones():
    settings = Settings(enable_student_extension=True)
    events = []
    answer = run_mock(
        "Compara el desempeno regional de Killa en Q3.",
        events.append,
        settings=settings,
    )
    assert "La Paz" in answer
    assert any(e.get("tool") == "comparar_regiones" for e in events)
    assert events[-1]["kind"] == "final"
