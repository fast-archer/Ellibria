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
    import json # Добавили импорт для чтения настроек
    config = _load_config()

    # 1. Читаем пользовательские настройки, если они есть
    USER_SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".ellibria-agent", "settings.json")
    user_lmstudio_url = config.LMSTUDIO_URL
    user_ollama_url = config.OLLAMA_URL
    
    if os.path.exists(USER_SETTINGS_PATH):
        try:
            with open(USER_SETTINGS_PATH, "r", encoding="utf-8") as f:
                user_data = json.load(f)
                if "lmStudioUrl" in user_data: user_lmstudio_url = user_data["lmStudioUrl"]
                if "ollamaUrl" in user_data: user_ollama_url = user_data["ollamaUrl"]
        except Exception:
            pass

    # Извлекаем базовый URL для пинга (обрезаем /v1 или /api)
    lm_ping = user_lmstudio_url.replace("/v1", "") if "/v1" in user_lmstudio_url else user_lmstudio_url
    ol_ping = user_ollama_url.replace("/v1", "").replace("/api", "") if "/v1" in user_ollama_url else user_ollama_url

    # 2. Проверка LM Studio
    if _ping(lm_ping):
        print(f"[AUTO] LM Studio обнаружен по адресу {lm_ping}")
        loaded_model = config.LOCAL_MODEL
        try:
            resp = requests.get(f"{lm_ping}/v1/models", timeout=1.5)
            if resp.status_code == 200:
                models_info = resp.json()
                if "data" in models_info and len(models_info["data"]) > 0:
                    loaded_model = models_info["data"][0]["id"]
        except Exception:
            pass 

        return (
            OpenAI(base_url=user_lmstudio_url.strip(), api_key="lm-studio"),
            loaded_model,
            "LM Studio (local)"
        )

    # 3. Проверка Ollama
    if _ping(ol_ping):
        print(f"[AUTO] Ollama обнаружен по адресу {ol_ping}")
        return (
            OpenAI(base_url=user_ollama_url.strip(), api_key="ollama"),
            config.LOCAL_MODEL,
            "Ollama (local)"
        )

    # 4. Проверка Gemini Flash
    if getattr(config, 'GEMINI_API_KEY', ''):
        print("[AUTO] Gemini Flash API")
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)
        return None, config.GEMINI_MODEL, "Gemini Flash (cloud)"

    # 5. Проверка Groq
    if getattr(config, 'GROQ_API_KEY', ''):
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