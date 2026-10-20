from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "ventas.csv"


def _load() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def comparar_regiones(producto: str, periodo: str = "Q3") -> dict:
    """Compara ingresos y unidades de un producto entre regiones en un periodo dado."""
    producto_clean = producto.strip()
    periodo_clean = periodo.upper().strip()

    df = _load()
    part = df[
        (df["trimestre"] == periodo_clean) & (df["producto"].str.lower() == producto_clean.lower())
    ]
    if part.empty:
        raise ValueError(
            f"No existen datos para el producto '{producto}' en el periodo '{periodo}'."
        )

    out = (
        part.groupby("region", as_index=False)
        .agg(ingresos=("ingresos", "sum"), unidades=("unidades", "sum"))
        .sort_values("ingresos", ascending=False)
    )
    records = out.round(2).to_dict(orient="records")
    region_lider = records[0] if records else None

    diferencia_pct = 0.0
    if len(records) >= 2:
        top_ingresos = records[0]["ingresos"]
        segundo_ingresos = records[1]["ingresos"]
        if segundo_ingresos > 0:
            diferencia_pct = round(((top_ingresos - segundo_ingresos) / segundo_ingresos) * 100, 2)

    ingresos_por_region = {r["region"]: r["ingresos"] for r in records}

    return {
        "producto": producto_clean,
        "periodo": periodo_clean,
        "region_lider": region_lider,
        "diferencia_pct_lider_vs_segundo": diferencia_pct,
        "ingresos_por_region": ingresos_por_region,
        "filas": records,
    }
