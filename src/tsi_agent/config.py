from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env", override=True)


@dataclass(frozen=True)
class Settings:
    provider: str = os.getenv("MODEL_PROVIDER", "mock").strip().lower()
    max_steps: int = int(os.getenv("AGENT_MAX_STEPS", "10"))
    enable_student_extension: bool = (
        os.getenv("ENABLE_STUDENT_EXTENSION", "false").lower() == "true"
    )

    azure_base_url: str = os.getenv("AZURE_OPENAI_BASE_URL", "").strip()
    azure_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
    azure_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
    azure_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()
    azure_api_version: str = os.getenv("OPENAI_API_VERSION", "").strip()

    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b").strip()
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()


def provider_readiness(provider: str, settings: Settings | None = None) -> tuple[bool, str]:
    s = settings or Settings()
    provider = provider.lower()
    if provider == "mock":
        return True, "Modo local determinista listo."
    if provider == "azure":
        if not s.azure_api_key or not s.azure_deployment:
            return False, "Faltan AZURE_OPENAI_API_KEY o AZURE_OPENAI_DEPLOYMENT."
        if not s.azure_base_url and not (s.azure_endpoint and s.azure_api_version):
            return (
                False,
                "Configure AZURE_OPENAI_BASE_URL o AZURE_OPENAI_ENDPOINT + OPENAI_API_VERSION.",
            )
        return True, "Configuracion Azure detectada."
    if provider == "ollama":
        return True, "Se intentara conectar al servicio Ollama configurado."
    return False, f"Proveedor no soportado: {provider}"
