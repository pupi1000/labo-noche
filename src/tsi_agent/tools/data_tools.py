from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = ROOT / "data" / "ventas.csv"


def _load() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def resumen_ventas(periodo: str = "Q3", agrupacion: str = "producto") -> dict:
    """Resume ingresos y unidades de un trimestre por producto o region."""
    periodo = periodo.upper().strip()
    agrupacion = agrupacion.lower().strip()
    if agrupacion not in {"producto", "region"}:
        raise ValueError("agrupacion debe ser 'producto' o 'region'")
    df = _load()
    part = df[df["trimestre"] == periodo]
    if part.empty:
        raise ValueError(f"Periodo inexistente: {periodo}")
    out = (
        part.groupby(agrupacion, as_index=False)
        .agg(ingresos=("ingresos", "sum"), unidades=("unidades", "sum"))
        .sort_values("ingresos", ascending=False)
    )
    return {
        "periodo": periodo,
        "agrupacion": agrupacion,
        "filas": out.round(2).to_dict(orient="records"),
    }


def comparar_periodos(
    periodo_inicial: str = "Q2",
    periodo_final: str = "Q3",
    agrupacion: str = "producto",
) -> dict:
    """Compara ingresos entre dos periodos y calcula variacion porcentual por grupo."""
    periodo_inicial = periodo_inicial.upper().strip()
    periodo_final = periodo_final.upper().strip()
    agrupacion = agrupacion.lower().strip()
    if agrupacion not in {"producto", "region"}:
        raise ValueError("agrupacion debe ser 'producto' o 'region'")
    df = _load()
    a = df[df["trimestre"] == periodo_inicial].groupby(agrupacion)["ingresos"].sum()
    b = df[df["trimestre"] == periodo_final].groupby(agrupacion)["ingresos"].sum()
    joined = pd.concat([a.rename("inicial"), b.rename("final")], axis=1).fillna(0)
    joined["variacion_pct"] = (
        (joined["final"] - joined["inicial"]) / joined["inicial"].replace(0, pd.NA)
    ) * 100
    joined = joined.reset_index().sort_values("variacion_pct", ascending=False)
    records = joined.round(2).to_dict(orient="records")
    top = records[0] if records else None
    return {
        "periodo_inicial": periodo_inicial,
        "periodo_final": periodo_final,
        "agrupacion": agrupacion,
        "mayor_crecimiento": top,
        "filas": records,
    }


def calcular_variacion(inicial: float, final: float) -> dict:
    """Calcula diferencia absoluta y variacion porcentual entre dos valores."""
    if inicial == 0:
        return {"inicial": inicial, "final": final, "diferencia": final, "variacion_pct": None}
    return {
        "inicial": inicial,
        "final": final,
        "diferencia": round(final - inicial, 4),
        "variacion_pct": round(((final - inicial) / inicial) * 100, 4),
    }
