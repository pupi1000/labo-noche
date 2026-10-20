from __future__ import annotations

from .config import Settings


def build_chat_model(provider: str, settings: Settings | None = None):
    s = settings or Settings()
    provider = provider.lower().strip()

    if provider == "azure":
        if s.azure_base_url:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=s.azure_deployment,
                base_url=s.azure_base_url,
                api_key=s.azure_api_key,
                temperature=0,
                use_responses_api=False,
            )

        from langchain_openai import AzureChatOpenAI

        return AzureChatOpenAI(
            azure_deployment=s.azure_deployment,
            azure_endpoint=s.azure_endpoint,
            api_version=s.azure_api_version,
            api_key=s.azure_api_key,
            temperature=0,
        )

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=s.ollama_model,
            base_url=s.ollama_base_url,
            temperature=0,
        )

    raise ValueError("build_chat_model solo se usa para azure u ollama")
