# Ellibria — AI Companion with Personality

<img src="https://github.com/fast-archer/echoai/blob/main/docs/screenshot.png" 
width="720" alt="Echo">

**Ellibria** is a locally-hosted AI agent with a distinctive personality engine,
persistent memory, and support for multiple backends — designed to feel less
like a tool and more like a presence.

---

## ✨ Features

- **Personality modes** — switch between Mistress, Mr. Robot, Psychotherapist,
  Loyal Friend, and more via the settings panel
- **Persistent memory** — conversations are summarized and retained between
  sessions, stored locally in `~/.echo-agent/`
- **Fully customizable system prompt** — rewrite her behavior from scratch
  in one click
- **Multiple themes** — Dark, Light, Purple, Night, Terminal
- **Voice output** — natural female TTS with language selection
- **Smart backend detection** — automatically connects to LM Studio, Ollama,
  Groq, or Gemini Flash depending on what's available
- **Secure local config** — API keys never leave your machine

---

## 🚀 Quick Start

### Windows (Recommended)

1. Download **[Ellibria Installer.exe](https://github.com/fast-archer/Ellibria/releases)**
2. Run the installer
3. On first launch, enter your **[Groq API Key](https://console.groq.com/keys)**
4. Echo starts immediately — no additional setup required

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
| Windows | `C:\Users\<You>\.echo-agent\` |
| Linux | `~/.echo-agent\` |

Files: `config.json`, `chat_history.json`, `system_prompt.txt`

---

## 🎨 Customization

Open **Settings** to adjust personality, voice, theme, and system prompt.
Echo adapts to whatever role or tone you configure.

---

## 📜 License

© 2026 Nikita Kayakhov. All rights reserved.  
Source code is available for viewing only.  
Commercial use or redistribution requires written permission.  
Contact: epidermis_essential@proton.me

---

## 🌐 Contact

- **Email**: epidermis_essential@proton.me  
- **Discord**: [Join server](https://discord.gg/yT8e83P4hz)
