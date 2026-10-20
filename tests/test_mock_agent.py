from tsi_agent.mock_agent import run_mock


def test_mock_genera_tool_calls_observables():
    events = []
    answer = run_mock(
        "Entre Q2 y Q3, que producto tuvo mayor crecimiento y que documentos lo explican?",
        events.append,
    )
    assert "Killa" in answer
    assert any(e.get("tool") == "comparar_periodos" for e in events)
    assert any(e.get("tool") == "buscar_documentos" for e in events)
    assert events[-1]["kind"] == "final"
