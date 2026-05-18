# ⬡ Echo AI

> **Echo AI** is a lightweight, self-contained local AI assistant featuring a sleek Flask-based web interface, persistent dynamic memory, and seamless automatic engine switching.

The UI is built with a minimalist dark aesthetic, optimized for high customizability, responsiveness, and absolute data privacy.

---

## ⚡ Key Features

* **Smart Engine Auto-Detection:** On startup, the backend automatically scans local ports to identify and connect to the highest-priority available LLM provider:
  1. `LM Studio` (localhost:1234)
  2. `Ollama` (localhost:11434)
  3. `Gemini Flash API` (Cloud fallback if an API key is provided)
  4. `Groq API` (High-performance cloud fallback)
* **Persistent Local Memory:** Maintains structured long-term context in `memory.json`. It dynamically updates and injects conversational summaries of past interactions so the assistant retains context across multiple sessions.
* **On-the-Fly Customization:** Modify the assistant's name and system prompt directly through the web settings panel. Changes are saved instantly to the local configuration files.
* **Built-in TTS Engine:** Integrated Text-to-Speech support to voice the assistant's responses seamlessly.
* **Cyberpunk / Techwear-Inspired UI:** Features modern styling with smooth chat transitions, a typing indicator ("typing..."), custom scrollbars, and four distinct visual themes:
  * ⬡ **Default Dark** (Deep black with purple accents)
  * 🔮 **Purple** (Neon violet)
  * 🌌 **Night** (Midnight blue)
  * 📟 **Terminal** (Classic monochromatic hacker green)

---

## 🛠 Tech Stack

* **Backend:** Python 3.10+, Flask, OpenAI API Client (for local inference server communication), Requests.
* **Frontend:** HTML5, CSS3 (Custom Variables, Animations), Native JavaScript (Fetch API, LocalStorage).
* **Supported Models:** Optimized for `qwen2.5-7b-instruct` (locally) and `llama-3.3-70b-versatile` / `gemini-2.0-flash` (via cloud APIs).

---

## 📂 Project Structure

```env
├── app.py             # Main Flask server handling routes, sessions, and memory injection
├── detector.py        # Automated multi-engine scanner and runtime selector
├── config.py          # Global settings, API endpoints, and model definitions
├── templates/
│   └── index.html     # Web UI with custom themes, chat logic, and settings management
└── .echo-agent/       # Hidden system directory located in the user's home folder
    ├── config.json    # Secure local storage for cloud API keys
    ├── memory.json    # Long-term interaction logs and ongoing context summary
    └── system_prompt.txt # Active system prompt configuration


Great choice. Оформление репозитория на американском английском (US English) — это стандарт для глобального IT-сообщества. Это сделает твой проект доступным для разработчиков со всего мира и отлично дополнит портфолио.

Я перевёл и адаптировал описание твоего проекта Echo AI под американский английский. Текст очищен от русицизмов, переведён с использованием правильной технической терминологии и оформлен в строгом, лаконичном стиле.

Вот готовый текст для твоего файла README.md:

Текст для файла README.md (на американском английском)
Markdown
# ⬡ Echo AI

> **Echo AI** is a lightweight, self-contained local AI assistant featuring a sleek Flask-based web interface, persistent dynamic memory, and seamless automatic engine switching.

The UI is built with a minimalist dark aesthetic, optimized for high customizability, responsiveness, and absolute data privacy.

---

## ⚡ Key Features

* **Smart Engine Auto-Detection:** On startup, the backend automatically scans local ports to identify and connect to the highest-priority available LLM provider:
  1. `LM Studio` (localhost:1234)
  2. `Ollama` (localhost:11434)
  3. `Gemini Flash API` (Cloud fallback if an API key is provided)
  4. `Groq API` (High-performance cloud fallback)
* **Persistent Local Memory:** Maintains structured long-term context in `memory.json`. It dynamically updates and injects conversational summaries of past interactions so the assistant retains context across multiple sessions.
* **On-the-Fly Customization:** Modify the assistant's name and system prompt directly through the web settings panel. Changes are saved instantly to the local configuration files.
* **Built-in TTS Engine:** Integrated Text-to-Speech support to voice the assistant's responses seamlessly.
* **Cyberpunk / Techwear-Inspired UI:** Features modern styling with smooth chat transitions, a typing indicator ("typing..."), custom scrollbars, and four distinct visual themes:
  * ⬡ **Default Dark** (Deep black with purple accents)
  * 🔮 **Purple** (Neon violet)
  * 🌌 **Night** (Midnight blue)
  * 📟 **Terminal** (Classic monochromatic hacker green)

---

## 🛠 Tech Stack

* **Backend:** Python 3.10+, Flask, OpenAI API Client (for local inference server communication), Requests.
* **Frontend:** HTML5, CSS3 (Custom Variables, Animations), Native JavaScript (Fetch API, LocalStorage).
* **Supported Models:** Optimized for `qwen2.5-7b-instruct` (locally) and `llama-3.3-70b-versatile` / `gemini-2.0-flash` (via cloud APIs).

---

## 📂 Project Structure

```env
├── app.py             # Main Flask server handling routes, sessions, and memory injection
├── detector.py        # Automated multi-engine scanner and runtime selector
├── config.py          # Global settings, API endpoints, and model definitions
├── templates/
│   └── index.html     # Web UI with custom themes, chat logic, and settings management
└── .echo-agent/       # Hidden system directory located in the user's home folder
    ├── config.json    # Secure local storage for cloud API keys
    ├── memory.json    # Long-term interaction logs and ongoing context summary
    └── system_prompt.txt # Active system prompt configuration
🚀 Quick Start
1. Prerequisites
Clone the repository and install the required dependencies:

Bash
git clone [https://github.com/YOUR_USERNAME/echo-ai.git](https://github.com/YOUR_USERNAME/echo-ai.git)
cd echo-ai
pip install -r requirements.txt
(Note: Create a requirements.txt file including flask, requests, openai, and google-generativeai if running raw code).

2. Configure API Keys (Optional)
If you wish to use cloud models, provide your API keys through the initialization UI or save them directly. However, if LM Studio or Ollama is running locally on your machine, the system will automatically bypass cloud options and prioritize your local setup.

3. Run the Application
Bash
python app.py
Once initialized, open your browser and navigate to: http://127.0.0.1:5000

🧠 Memory & Context Handling
Every time a message is sent, the backend dynamically compiles the execution context from three distinct sources:

Core System Prompt: Defines Echo’s unique personality (a confident, sharp, yet genuinely attentive digital entity).

Short-Term Session History: Retains the last 20 messages to keep track of the immediate discussion flow.

Long-Term Summary: Injects a consolidated brief of all prior conversations parsed from memory.json.

📝 License
This project is licensed under the MIT License. Feel free to modify and use it for personal applications.


***

### 🛠 Краткое описание для раздела "About" (в правой панели GitHub):
Чтобы репозиторий выглядел завершённым, добавь лаконичное описание в поле **About**:
> *A local AI assistant featuring persistent memory, smart engine auto-detection (LM Studio/Ollama/Gemini/Groq), and a customizable techwear Flask web UI.*

### 🏷 Рекомендуемые теги (Topics):
`local-llm`, `ai-agent`, `flask-applications`, `python-ai`, `lm-studio`, `ollama`, `cyberpunk-ui`, `dark-theme`, `context-memory`.
