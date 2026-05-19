import requests
import importlib.util
import sys
import os

def _load_config():
    """Грузит config.py из папки рядом с exe или скриптом."""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base, "config.py")

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"config.py не найден рядом с программой!\n"
            f"Ожидался по пути: {config_path}\n\n"
            f"Скачай config.py из репозитория и положи рядом с exe."
        )

    spec = importlib.util.spec_from_file_location("config", config_path)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg

def _ping(url, timeout=2):
    try:
        requests.get(url.strip(), timeout=timeout)
        return True
    except Exception:
        return False

def get_engine():
    """Возвращает (client, model, engine_name). Пробует варианты по приоритету."""
    from openai import OpenAI
    config = _load_config()

    # Сначала проверяем, есть ли живой ключ прямо в системном окружении процесса
    env_groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    # Если в окружении пусто, пробуем взять из config.py
    groq_key = env_groq_key if env_groq_key else getattr(config, 'GROQ_API_KEY', '').strip()

    env_gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    gemini_key = env_gemini_key if env_gemini_key else getattr(config, 'GEMINI_API_KEY', '').strip()

    # 1. LM Studio
    if _ping("http://localhost:1234"):
        print("[AUTO] LM Studio обнаружен → локальная модель")
        return (
            OpenAI(base_url=config.LMSTUDIO_URL.strip(), api_key="lm-studio"),
            config.LOCAL_MODEL,
            "LM Studio (local)"
        )

    # 2. Ollama
    if _ping("http://localhost:11434"):
        print("[AUTO] Ollama обнаружен → локальная модель")
        return (
            OpenAI(base_url=config.OLLAMA_URL.strip(), api_key="ollama"),
            config.LOCAL_MODEL,
            "Ollama (local)"
        )

    # 3. Gemini Flash
    if gemini_key:
        print("[AUTO] Gemini Flash API")
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        return None, config.GEMINI_MODEL, "Gemini Flash (cloud)"

    # 4. Groq (по умолчанию, если ключ есть)
    if groq_key:
        print("[AUTO] Groq API")
        return (
            OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=groq_key  # <-- Теперь тут гарантированно ЧИСТЫЙ и СВЕЖИЙ ключ!
            ),
            config.GROQ_MODEL,
            "Groq (cloud)"
        )

    raise RuntimeError(
        "Нет доступного движка!\n"
        "Запусти LM Studio/Ollama или добавь API-ключ в config.py"
    )
