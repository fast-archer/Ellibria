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

def _get_active_groq_model(api_key, fallback_model):
    """Динамически запрашивает список активных моделей у Groq, предотвращая ошибку 404."""
    try:
        url = "https://api.groq.com/openai/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            models_data = response.json().get("data", [])
            model_ids = [m["id"] for m in models_data if "embed" not in m["id"] and "guard" not in m["id"]]
            
            # Приоритетный выбор самых стабильных быстрых моделей
            for preferred in ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "llama-3.1-70b-versatile"]:
                if preferred in model_ids:
                    return preferred
            
            if model_ids:
                return model_ids[0]
    except Exception:
        pass
    
    return fallback_model

def get_engine():
    """Возвращает (client, model, engine_name). Пробует варианты по приоритету."""
    from openai import OpenAI
    import json
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

    # 5. Проверка Groq (теперь с авто-опросом моделей)
    groq_key = getattr(config, 'GROQ_API_KEY', '')
    if groq_key:
        print("[AUTO] Groq API")
        active_groq_model = _get_active_groq_model(groq_key, config.GROQ_MODEL)
        return (
            OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=groq_key
            ),
            active_groq_model,
            "Groq (cloud)"
        )

    raise RuntimeError(
        "Нет доступного движка!\n"
        "Запусти LM Studio/Ollama или добавь API-ключ в config.py"
    )