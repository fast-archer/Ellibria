### Ellibria — AI Companion with Personality

<img src="https://github.com/fast-archer/Ellibria/blob/main/docs/screenshot.png" 
width="720" alt="Ellibria">

**[Ellibria](https://fast-archer.github.io/Ellibria/)** is a locally-hosted AI agent with a distinctive personality engine,
persistent memory, and support for multiple backends — designed to feel less
like a tool and more like a presence.

---

## 🚀 Features

### 🎙️ Advanced Voice & Interaction
* **Interactive Voice HUD [New]** — An elegant, central screen overlay with a live CSS audio wave animation that triggers instantly during Speech-to-Text input.
* **Theme-Aware Voice UI [New]** — The recording panel dynamically adapts to your active UI theme using native CSS variables, preserving visual balance.
* **Voice Output** — Natural female Text-to-Speech (TTS) with smooth language selection.
* **Liked Responses as Style Memory** — Heart a response and Ellibria learns your preferred tone and communication style over time.

### 🧠 Personality & Core Intelligence
* **Personality Modes** — Switch between Custom, Dommy, Hacker, Critic, Pick-Me, Therapist, Friend, and more via the settings panel.
* **Smart Language Lock [New]** — Automated system prompt guards that prevent local models from mixing languages mid-sentence or introducing unintended scripts (e.g., Asian glyphs) unless requested.
* **Personality Archive** — Persistent facts about you, automatically updated after each conversation and fully editable.
* **Fully Customizable System Prompt** — Rewrite her core behavior and rules from scratch in a single click.

### 🛠️ Architecture & Performance Safety
* **Safe Mode for Local Models [New]** — Integrated memory protection layer toggle designed to prevent PC freezes and VRAM overflows on weaker GPUs (VRAM < 6GB) during extended sessions.
* **Robust Response Parsing [New]** — Internal protective filter that automatically strips Markdown code blocks from local model outputs, eliminating JSON parser crashes.
* **Multithreaded Architecture** — Keeps the UI responsive during heavy background processing, generation, or text truncation.
* **Graceful Vision API Handling [New]** — Robust error guards for Vision workflows that seamlessly catch API rate limits (e.g., 429 Too Many Requests) without breaking the execution pipeline.

### 📂 Data Control & Ecosystem
* **Full Data Control** — Export, import, and manually edit your profile archive and conversation backups at any time.
* **Persistent Memory** — Conversations are summarized and cleanly retained between sessions, stored locally in `%USERPROFILE%/.ellibria-agent/`.
* **Search with Navigation** — Easily search through chat history and jump directly to the matched message bubble.
* **Automatic Port Selection** — No port conflicts if default ports are occupied; background engine handles assignment smoothly.
* **Fully Offline Assets** — Zero CDN dependencies; all style sheets, scripts, and interface components are bundled locally.
* **Secure Local Config** — Your private API keys never leave your machine.
* **Smart Backend Detection** — Automatically detects and connects to LM Studio, Ollama, Groq, or Gemini Flash depending on what's available.

---

## 🚀 Quick Start

### Windows (Recommended)

1. Download **[Ellibria Installer.exe](https://github.com/fast-archer/Ellibria/releases)**
2. Run the installer
3. On first launch, enter your **[Groq API Key](https://console.groq.com/keys)**
4. Ellibria starts immediately — no additional setup required

### Linux / Arch Linux

Full one-click Linux installer coming soon.

---

## 🔧 Supported Backends

| Backend | Type | Notes |
|---|---|---|
| LM Studio | Local | Best for privacy |
| Ollama | Local | Lightweight alternative |
| Groq | Cloud | Fast, free tier available |
| Gemini Flash | Cloud | Google API |

Auto-detected on startup — no manual configuration needed.

---

## 📁 Data Storage

All data is stored locally on your machine:

| Platform | Path |
|---|---|
| Windows | `C:\Users\<You>\.ellibria-agent\` |
| Linux   | `~/.ellibria-agent\`              |

Files: `config.json`, `sessions.json`, `memory.json`, `system_prompt.txt`, `user_profile.json`, `liked_messages.json`, `error.log`

---

## 🎨 Customization

Open **Settings** to adjust personality, voice, theme, and system prompt.
Ellibria adapts to whatever role or tone you configure.

---

## 📜 License

© 2026 Nikita Kayakhov. All rights reserved.  
Source code is available for viewing only.  
Commercial use or redistribution requires written permission.  
Contact: epidermis_essential@proton.me

---

## 🌐 Contact

- **Email**: epidermis_essential@proton.me  
