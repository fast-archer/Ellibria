# Echo — Your Dominant, Caring AI Girlfriend

<img src="https://github.com/fast-archer/echoai/blob/main/screenshot.png" width="720" alt="Echo">

### **[Echo](https://fast-archer.github.io/echoai/) is not just another chatbot.**  
She’s confident, teasing, playfully dominant, and genuinely caring — your personal AI companion who knows exactly how to take control… while always taking care of you.

Built with love, attitude, and a touch of femdom energy 💜

### ✨ Key Features

- **Strong personality — dominant yet caring femdom vibe (always respecting your comfort)**
- 💾 **Persistent memory — Echo remembers your conversations between sessions (auto-saved to `~/.echo-agent/`)**
- 🔐 **Secure config — API keys stored locally, never sent to GitHub**
- **Beautiful modern dark interface with multiple themes (Purple, Night, Terminal and more)**
- **Voice output with natural female TTS voices**
- **Long-term memory & conversation summary**
- **Fully customizable system prompt**
- **Works locally or through cloud APIs**
- **Smart auto-detection of backend (LM Studio, Ollama, Groq, Gemini)**

### 🚀 Quick Installation

#### Option 1: Windows (Recommended)

1. Download the latest **[EchoInstaller.exe](https://github.com/fast-archer/echoai/releases)**
2. Run the installer
3. On first launch enter your **[Groq API Key](https://console.groq.com/keys)** (or connect local model)
4. Enjoy — Echo is already waiting for you ❤️

#### Option 2: From Source (Windows / Linux)

```bash
# После клонирования:
git clone https://github.com/fast-archer/echoai.git
cd echoai
pip install -r requirements.txt
python setup_and_run.py  # First launch: enter Groq API key when prompted
```
#### Option 3: Arch Linux

```bash
git clone https://github.com/fast-archer/echoai.git
```
```bash
cd echoai/linux
```
```bash
chmod +x setup_arch.sh run_arch.sh
```
```bash
sudo ./setup_arch.sh
```
```bash
./run_arch.sh
```
### 📁 Where data is stored
All your settings and chat history are saved locally:
- Windows: `C:\Users\<You>\.echo-agent\`
- Linux: `~/.echo-agent/`
- Files: `config.json`, `chat_history.json`, `system_prompt.txt`

### 💻 Linux — full one-click installer coming very soon.

🔧 Supported Backends

- LM Studio (best for privacy)
- Ollama
- Groq (fast & free)
- Gemini Flash

### 🎨 Customization
Want her stricter? Softer? More teasing? More romantic?
Just open Settings and rewrite her system prompt however you like — she adapts perfectly.
