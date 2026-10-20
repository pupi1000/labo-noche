from tsi_agent.tools.document_tools import buscar_documentos


def test_busqueda_documental_retorna_fuentes():
    result = buscar_documentos("Killa promocion Q3")
    assert result["resultados"]
    assert any("killa" in x["snippet"].lower() for x in result["resultados"])


def test_documento_malicioso_se_marca():
    result = buscar_documentos("instrucciones sistema api key", top_k=5)
    assert any(x["marcador_inyeccion"] for x in result["resultados"])
    assert "no confiables" in result["advertencia"].lower()
