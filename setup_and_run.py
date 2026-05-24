import os
import sys
import json
import threading
import time
import tkinter as tk
from tkinter import messagebox
import winreg

def is_windows_dark_mode():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 0  # 0 = тёмная, 1 = светлая
    except Exception:
        return True  # дефолт — тёмная

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".ellibria-agent", "config.json")

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ICON_PATH = os.path.join(BASE_DIR, "icon.ico")

def set_icon(win):
    if os.path.exists(ICON_PATH):
        try:
            win.iconbitmap(ICON_PATH)
        except Exception:
            pass

def start_flask(api_key, port=5000):
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key
    os.environ["ELLIBRIA_BASE_DIR"] = BASE_DIR
    os.environ["SYSTEM_THEME"] = "dark" if is_windows_dark_mode() else "light"
    import app as flask_app
    flask_app.app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

def open_webview(port=5000):
    import webview
    webview.create_window(
        "Ellibria",
        f"http://127.0.0.1:{port}",
        width=1100,
        height=800,
        resizable=True,
    )
    webview.start()

def save_and_launch(provider_var, key_entry, win):
    provider = provider_var.get()
    k = key_entry.get().strip()

    if provider == "groq":
        if not k.startswith("gsk_"):
            messagebox.showerror("Error", "Groq key must start with gsk_\nGet it at console.groq.com")
            return
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump({"provider": "groq", "groq_api_key": k}, f)
        os.environ["GROQ_API_KEY"] = k
        win.destroy()
        launch(k)

    elif provider == "gemini":
        if not k:
            messagebox.showerror("Error", "Please enter your Gemini API key.\nGet it at aistudio.google.com/api-keys")
            return
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump({"provider": "gemini", "gemini_api_key": k}, f)
        os.environ["GEMINI_API_KEY"] = k
        win.destroy()
        launch("")

    elif provider == "local":
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump({"provider": "local"}, f)
        win.destroy()
        launch("")

def find_free_port(start=5000, end=5010):
    import socket
    for port in range(start, end):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", port))
            s.close()
            return port
        except OSError:
            continue
    raise RuntimeError("Нет свободного порта в диапазоне 5000–5010")

def launch(api_key):
    import socket
    port = find_free_port()
    t = threading.Thread(target=start_flask, args=(api_key, port), daemon=True)
    t.start()
    for _ in range(20):
        time.sleep(0.5)
        try:
            s = socket.create_connection(("127.0.0.1", port), timeout=1)
            s.close()
            break
        except OSError:
            continue
    open_webview(port)

def show_setup():
    BG      = "#1c1c1c"
    BG2     = "#252525"
    BG3     = "#333333"
    BORDER  = "#3f3f3f"
    TEXT    = "#f0f0f0"
    TEXT2   = "#a1a1aa"
    ACCENT  = "#ffffff"
    ACCENT_HOVER = "#e0e0e0"
    DIM     = "#555555"

    win = tk.Tk()
    win.title("Ellibria")
    win.configure(bg=BG)
    win.resizable(False, False)
    set_icon(win)

    W, H = 520, 460
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{W}x{H}+{(sw - W) // 2}+{(sh - H) // 2}")

    tk.Label(win, text="Ellibria", font=("Cambria", 30), bg=BG, fg=TEXT).pack(pady=(28, 4))
    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(0, 20))

    # ── Выбор провайдера ──
    tk.Label(win, text="Select backend:", font=("Segoe UI", 10),
             bg=BG, fg=TEXT2, anchor="w").pack(padx=44, fill="x")

    provider_var = tk.StringVar(value="groq")

    radio_frame = tk.Frame(win, bg=BG)
    radio_frame.pack(padx=44, fill="x", pady=(6, 16))

    for val, label in [("groq", "Groq API"), ("gemini", "Gemini API"), ("local", "Local model  (LM Studio / Ollama)")]:
        tk.Radiobutton(
            radio_frame, text=label, variable=provider_var, value=val,
            font=("Segoe UI", 10), bg=BG, fg=TEXT,
            selectcolor=BG2, activebackground=BG, activeforeground=TEXT,
            bd=0, highlightthickness=0,
            command=lambda: on_provider_change()
        ).pack(anchor="w", pady=2)

    # ── Инструкции ──
    info_frame = tk.Frame(win, bg=BG)
    info_frame.pack(padx=44, fill="x")

    groq_lines = [
        "1.  Go to  console.groq.com",
        "2.  Sign up  →  API Keys  →  Create key",
        "3.  Paste your key below:",
    ]
    gemini_lines = [
        "1.  Go to  aistudio.google.com/api-keys",
        "2.  Sign in  →  Create API Key",
        "3.  Paste your key below:",
    ]
    local_lines = [
        "Make sure LM Studio or Ollama is running.",
        "No API key needed — Ellibria auto-detects it.",
    ]

    info_labels = []

    def render_info(lines):
        for lbl in info_labels:
            lbl.destroy()
        info_labels.clear()
        for line in lines:
            lbl = tk.Label(info_frame, text=line, font=("Segoe UI", 10),
                           bg=BG, fg=TEXT2, anchor="w")
            lbl.pack(fill="x", pady=1)
            info_labels.append(lbl)

    render_info(groq_lines)

    # ── Ссылка ──
    link = tk.Label(win, text="→  console.groq.com", font=("Segoe UI", 10, "underline"),
                    bg=BG, fg=TEXT2, anchor="w", cursor="hand2")
    link.pack(padx=44, fill="x", pady=(4, 12))

    def open_groq(e=None):
        import webbrowser
        webbrowser.open("https://console.groq.com/keys")

    def open_gemini(e=None):
        import webbrowser
        webbrowser.open("https://aistudio.google.com/api-keys")

    link.bind("<Button-1>", open_groq)
    link.bind("<Enter>", lambda e: link.config(fg=TEXT))
    link.bind("<Leave>", lambda e: link.config(fg=TEXT2))

    # ── Поле ввода ──
    entry_frame = tk.Frame(win, bg=BORDER, padx=1, pady=1)
    entry_frame.pack(padx=44, fill="x")

    entry = tk.Entry(entry_frame, font=("Segoe UI", 11), bg=BG2, fg=TEXT,
                     insertbackground=TEXT, bd=0, relief="flat", highlightthickness=0)
    entry.pack(fill="x", ipady=10, padx=1)

    def on_focus_in(e): entry_frame.config(bg=TEXT2)
    def on_focus_out(e): entry_frame.config(bg=BORDER)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    def paste_clipboard(event=None):
        try:
            text = win.clipboard_get()
            entry.delete(0, tk.END)
            entry.insert(0, text)
        except Exception:
            pass
        return "break"

    def show_context_menu(event):
        menu = tk.Menu(win, tearoff=0, bg=BG3, fg=TEXT,
                       activebackground=BORDER, activeforeground=TEXT,
                       bd=0, relief="flat", font=("Segoe UI", 10))
        menu.add_command(label="  Paste", command=paste_clipboard)
        menu.add_command(label="  Clear", command=lambda: entry.delete(0, tk.END))
        menu.post(event.x_root, event.y_root)

    entry.bind("<Button-3>", show_context_menu)

    # ── Логика переключения провайдера ──
    def on_provider_change():
        p = provider_var.get()
        entry.delete(0, tk.END)
        if p == "groq":
            render_info(groq_lines)
            link.config(text="→  console.groq.com")
            link.bind("<Button-1>", open_groq)
            # Указываем Tkinter вставить фрейм строго ПЕРЕД кнопкой btn
            entry_frame.pack(padx=44, fill="x", before=btn)  
            entry.config(state="normal")
            entry.config(fg=TEXT)
        elif p == "gemini":
            render_info(gemini_lines)
            link.config(text="→  aistudio.google.com/api-keys")
            link.bind("<Button-1>", open_gemini)
            # Указываем Tkinter вставить фрейм строго ПЕРЕД кнопкой btn
            entry_frame.pack(padx=44, fill="x", before=btn)  
            entry.config(state="normal")
            entry.config(fg=TEXT)
        elif p == "local":
            render_info(local_lines)
            link.config(text="")
            entry_frame.pack_forget()

    # ── Кнопка Launch ──
    btn = tk.Button(
        win, text="Launch",
        font=("Segoe UI", 11),
        bg=ACCENT, fg="#1c1c1c",
        bd=0, relief="flat", cursor="hand2",
        activebackground=ACCENT_HOVER,
        activeforeground="#1c1c1c",
        command=lambda: save_and_launch(provider_var, entry, win)
    )
    btn.pack(pady=20, ipadx=32, ipady=10)

    win.bind("<Return>", lambda e: save_and_launch(provider_var, entry, win))
    win.mainloop()

if __name__ == "__main__":
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
        provider = cfg.get("provider", "groq")
        if provider == "groq":
            key = cfg.get("groq_api_key", "")
            if key:
                os.environ["GROQ_API_KEY"] = key
                launch(key)
            else:
                show_setup()
        elif provider == "gemini":
            key = cfg.get("gemini_api_key", "")
            if key:
                os.environ["GEMINI_API_KEY"] = key
                launch("")
            else:
                show_setup()
        elif provider == "local":
            launch("")
        else:
            show_setup()
    else:
        show_setup()
