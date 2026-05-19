import os
import json
from datetime import datetime

# Вытаскиваем ключ ИЗНАЧАЛЬНО
DATA_DIR = os.path.join(os.path.expanduser("~"), ".echo-agent")
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")

if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH) as f:
            config_data = json.load(f)
            if "groq_api_key" in config_data:
                clean_key = str(config_data["groq_api_key"]).strip().replace("\r", "").replace("\n", "")
                os.environ["GROQ_API_KEY"] = clean_key
    except Exception:
        pass

from flask import Flask, request, jsonify, render_template
from detector import get_engine

app = Flask(__name__)
app.secret_key = "echo-secret-key-2026-random"

# Автодетект движка
client, MODEL, ENGINE = get_engine()

MEMORY_PATH = os.path.join(DATA_DIR, "memory.json")
PROMPT_PATH = os.path.join(DATA_DIR, "system_prompt.txt")
HISTORY_PATH = os.path.join(DATA_DIR, "chat_history.json")

DEFAULT_PROMPT = "You are Echo. Dominate and care. Respond briefly and to the point."

def load_system_prompt():
    if os.path.exists(PROMPT_PATH):
        try:
            with open(PROMPT_PATH, encoding="utf-8") as f:
                content = f.read().strip()
                return content if content else DEFAULT_PROMPT
        except Exception:
            pass
    return DEFAULT_PROMPT

SYSTEM_PROMPT = load_system_prompt()

def load_chat_history():
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, encoding="utf-8") as f:
                history = json.load(f)
                return history[-20:] if isinstance(history, list) else []
        except Exception:
            pass
    return []

def save_chat_history(history):
    try:
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(history[-20:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠ Не удалось сохранить историю: {e}")

def save_memory(user_msg, bot_msg):
    try:
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, encoding="utf-8") as f:
                mem = json.load(f)
        else:
            mem = {"summary": "", "last_seen": None}
        mem["last_seen"] = datetime.now().isoformat()
        entry = f"[{datetime.now().strftime('%d.%m %H:%M')}] User: {user_msg[:40]}... | Echo: {bot_msg[:40]}..."
        lines = mem.get("summary", "").split("\n")
        lines.append(entry)
        mem["summary"] = "\n".join(lines[-25:])
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(mem, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ── Генерация ответа с Дебагом ────────────────────────────
def generate(messages_for_llm):
    if "Gemini" in ENGINE:
        import google.generativeai as genai
        model = genai.GenerativeModel(MODEL, system_instruction=messages_for_llm[0]["content"])
        history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in messages_for_llm[1:-1]]
        chat = model.start_chat(history=history)
        resp = chat.send_message(messages_for_llm[-1]["content"])
        return resp.text.strip()
    else:
        from openai import OpenAI
        from detector import _get_saved_groq_key
        
        # ЛОГ ПЕРЕД САМОЙ ОТПРАВКОЙ ЗАПРОСА В ДВИЖОК
        local_key = os.environ.get("GROQ_API_KEY", "").strip()
        file_key = _get_saved_groq_key()
        
        print("\n--- [DEBUG GENERATE] ---")
        print(f"Поток выполнения запроса. Использован движок: {ENGINE}")
        print(f"Ключ из os.environ текущего потока: {local_key[:12]}... (Длина: {len(local_key)})")
        print(f"Ключ напрямую из config.json: {file_key[:12]}... (Длина: {len(file_key)})")
        
        final_key = local_key if local_key else file_key
        print(f"Итоговый ключ, передаваемый в OpenAI(): {final_key[:12]}...")
        print("------------------------\n")
        
        thread_client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=final_key
        )
        
        resp = thread_client.chat.completions.create(
            model=MODEL,
            messages=messages_for_llm,
            max_tokens=700,
            temperature=0.8
        )
        return resp.choices[0].message.content.strip()

# ── Роуты ───────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", engine=ENGINE)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "empty"}), 400

    print(f"\n[DEBUG ROUTE] Получен запрос из браузера. Текст: '{user_msg}'")

    history = load_chat_history()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_msg}
    ]

    try:
        bot_msg = generate(messages)
    except Exception as e:
        import traceback
        print("\n❌ !!! [КРИТИЧЕСКАЯ ОШИБКА ДВИЖКА В ТЕРМИНАЛЕ] !!!")
        traceback.print_exc()  # Печатает полный системный трейсбэк ошибки
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        return jsonify({"error": f"Ошибка движка: {str(e)}"}), 503

    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": bot_msg})
    save_chat_history(history)
    save_memory(user_msg, bot_msg)

    return jsonify({"response": bot_msg, "engine": ENGINE})

@app.route("/set_prompt", methods=["POST"])
def set_prompt():
    global SYSTEM_PROMPT
    new_prompt = request.json.get("system_prompt", "").strip()
    if new_prompt:
        SYSTEM_PROMPT = new_prompt
        try:
            with open(PROMPT_PATH, "w", encoding="utf-8") as f:
                f.write(new_prompt)
        except Exception:
            pass
    return jsonify({"ok": True})

@app.route("/reset_prompt", methods=["POST"])
def reset_prompt():
    global SYSTEM_PROMPT
    SYSTEM_PROMPT = DEFAULT_PROMPT
    try:
        with open(PROMPT_PATH, "w", encoding="utf-8") as f:
            f.write(DEFAULT_PROMPT)
    except Exception:
        pass
    return jsonify({"ok": True, "prompt": DEFAULT_PROMPT})

@app.route("/reset", methods=["POST"])
def reset():
    save_chat_history([])
    return jsonify({"ok": True})

if __name__ == "__main__":
    print(f"\n✓ Движок при старте app.py: {ENGINE}")
    print(f"✓ Модель при старте app.py: {MODEL}\n")
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)
