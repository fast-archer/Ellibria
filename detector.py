import requests
import importlib.util
import sys
import os
import json

DATA_DIR = os.path.join(os.path.expanduser("~"), ".echo-agent")
CONFIG_JSON_PATH = os.path.join(DATA_DIR, "config.json")

def _load_config():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base, "config.py")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"config.py не найден по пути: {config_path}")

    spec = importlib.util.spec_from_file_location("config", config_path)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg

def _get_saved_groq_key():
    if os.path.exists(CONFIG_JSON_PATH):
        try:
            with open(CONFIG_JSON_PATH) as f:
                data = json.load(f)
                return str(data.get("groq_api_key", "")).strip().replace("\r", "").replace("\n", "")
        except Exception:
            pass
    return ""

def _ping(url, timeout=2):
    try:
        requests.get(url.strip(), timeout=timeout)
        return True
    except Exception:
        return False

def get_engine():
    from openai import OpenAI
    config = _load_config()

    if _ping("http://localhost:1234"):
        return OpenAI(base_url=config.LMSTUDIO_URL.strip(), api_key="lm-studio"), config.LOCAL_MODEL, "LM Studio (local)"

    if _ping("http://localhost:11434"):
        return OpenAI(base_url=config.OLLAMA_URL.strip(), api_key="ollama"), config.LOCAL_MODEL, "Ollama (local)"

    env_gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    gemini_key = env_gemini_key if env_gemini_key else getattr(config, 'GEMINI_API_KEY', '').strip()
    if gemini_key:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        return None, config.GEMINI_MODEL, "Gemini Flash (cloud)"

    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not groq_key:
        groq_key = _get_saved_groq_key()
    if not groq_key:
        groq_key = getattr(config, 'GROQ_API_KEY', '').strip()

    if groq_key:
        print(f"[DETECTOR] Инициализация Groq при запуске. Длина ключа: {len(groq_key)}")
        return (
            OpenAI(base_url="https://api.groq.com/openai/v1", api_key=groq_key),
            config.GROQ_MODEL,
            "Groq (cloud)"
        )

    raise RuntimeError("Нет доступного движка! Проверьте ключи.")
