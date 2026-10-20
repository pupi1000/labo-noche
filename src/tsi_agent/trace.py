from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / "logs"


def save_trace(question: str, provider: str, events: list[dict], answer: str) -> Path:
    LOGS.mkdir(exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = LOGS / f"trace_{stamp}.json"
    payload = {
        "created_at_utc": datetime.now(UTC).isoformat(),
        "provider": provider,
        "question": question,
        "events": events,
        "final_answer": answer,
        "note": "La traza registra acciones observables; no incluye chain-of-thought.",
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return path
