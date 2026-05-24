import os

from langchain_openai import ChatOpenAI


def create_chat_model(temperature: float = 0.1):
    os.environ.setdefault("NO_PROXY", "127.0.0.1,localhost")
    os.environ.setdefault("no_proxy", "127.0.0.1,localhost")

    provider = os.getenv("LLM_PROVIDER", "").lower()
    base_url = os.getenv("BASE_URL", "")
    model = os.getenv("MODEL", "qwen-plus")

    if provider == "ollama" or "11434" in base_url:
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=model,
            base_url=base_url.replace("/v1", "") or "http://127.0.0.1:11434",
            temperature=temperature,
        )

    return ChatOpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model=model,
        base_url=base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=temperature,
    )
