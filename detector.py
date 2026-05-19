import requests, importlib.util, sys, os

def _load_config():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))  # ✅ __file__
    config_path = os.path.join(base, "config.py")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"config.py not found next to the program!\nExpected: {config_path}"
        )
    
    spec = importlib.util.spec_from_file_location("config", config_path)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg

def _ping(url, timeout=2):
    try:
        requests.get(url.strip(), timeout=timeout)  # ✅ убран пробел
        return True
    except:
        return False

def get_engine():
    from openai import OpenAI
    config = _load_config()
    
    if _ping("http://localhost:1234"):  # ✅ убран пробел
        print("[AUTO] LM Studio detected")
        return OpenAI(base_url=config.LMSTUDIO_URL.strip(), api_key="lm-studio"), config.LOCAL_MODEL, "LM Studio"
    
    if _ping("http://localhost:11434"):  # ✅ убран пробел
        print("[AUTO] Ollama detected")
        return OpenAI(base_url=config.OLLAMA_URL.strip(), api_key="ollama"), config.LOCAL_MODEL, "Ollama"
    
    if getattr(config, 'GEMINI_API_KEY', ''):
        print("[AUTO] Gemini Flash")
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)
        return None, config.GEMINI_MODEL, "Gemini"
    
    if getattr(config, 'GROQ_API_KEY', ''):
        print("[AUTO] Groq API")
        return OpenAI(base_url="https://api.groq.com/openai/v1", api_key=config.GROQ_API_KEY), config.GROQ_MODEL, "Groq"
    
    raise RuntimeError("No engine available. Start LM Studio/Ollama or add API key to config.py")
