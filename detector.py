import requests
import config

def _ping(url, timeout=2):
    try:
        requests.get(url, timeout=timeout)
        return True
    except Exception:
        return False

def get_engine():
    """
    Возвращает (client, model, engine_name).
    Пробует варианты по приоритету.
    """
    from openai import OpenAI

    # 1. LM Studio
    if _ping("http://localhost:1234"):
        print("[AUTO] LM Studio обнаружен → локальная модель")
        return (
            OpenAI(base_url=config.LMSTUDIO_URL, api_key="lm-studio"),
            config.LOCAL_MODEL,
            "LM Studio (local)"
        )

    # 2. Ollama
    if _ping("http://localhost:11434"):
        print("[AUTO] Ollama обнаружен → локальная модель")
        return (
            OpenAI(base_url=config.OLLAMA_URL, api_key="ollama"),
            config.LOCAL_MODEL,
            "Ollama (local)"
        )

    # 3. Gemini Flash (самый щедрый бесплатный)
    if config.GEMINI_API_KEY:
        print("[AUTO] Gemini Flash API")
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)
        return (None, config.GEMINI_MODEL, "Gemini Flash (cloud)")

    # 4. Groq
    if config.GROQ_API_KEY:
        print("[AUTO] Groq API")
        return (
            OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=config.GROQ_API_KEY
            ),
            config.GROQ_MODEL,
            "Groq (cloud)"
        )

    raise RuntimeError(
        "Нет доступного движка!\n"
        "Запусти LM Studio/Ollama или добавь API-ключ в config.py"
    )