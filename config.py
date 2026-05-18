import os

GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
GEMINI_API_KEY = ""

LOCAL_MODEL  = "qwen2.5-7b-instruct"
GROQ_MODEL   = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-2.0-flash"

LMSTUDIO_URL = "http://localhost:1234/v1"
OLLAMA_URL   = "http://localhost:11434/v1"
