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

def save_and_launch(key, win):
    k = key.strip()
    if not k.startswith("gsk_"):
        messagebox.showerror("Error", "Key must start with gsk_\nGet it at console.groq.com")
        return
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"groq_api_key": k}, f)
    win.destroy()
    launch(k)

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
    # Цвета из index.html dark theme
    BG      = "#1c1c1c"
    BG2     = "#252525"
    BG3     = "#333333"
    BORDER  = "#3f3f3f"
    TEXT    = "#f0f0f0"
    TEXT2   = "#a1a1aa"
    ACCENT  = "#ffffff"
    ACCENT_HOVER = "#e0e0e0"

    win = tk.Tk()
    win.title("Ellibria")
    win.configure(bg=BG)
    win.resizable(False, False)
    set_icon(win)

    # Центрируем окно на экране
    W, H = 500, 360
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{W}x{H}+{(sw - W) // 2}+{(sh - H) // 2}")

    # ── Заголовок «Ellibria» шрифтом Cambria как в index.html ──
    tk.Label(
        win, text="Ellibria",
        font=("Cambria", 30),
        bg=BG, fg=TEXT
    ).pack(pady=(32, 4))

    # Тонкая разделительная линия под заголовком
    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=40, pady=(0, 24))

    # Инструкция
    for line in (
        "1.  Go to  console.groq.com",
        "2.  Sign up  →  API Keys  →  Create key",
        "3.  Paste your key below:",
    ):
        tk.Label(
            win, text=line,
            font=("Segoe UI", 10),
            bg=BG, fg=TEXT2, anchor="w"
        ).pack(padx=44, fill="x", pady=1)

    # Кликабельная ссылка
    link = tk.Label(
        win, text="→  console.groq.com",
        font=("Segoe UI", 10, "underline"),
        bg=BG, fg=TEXT2, anchor="w", cursor="hand2"
    )
    link.pack(padx=44, fill="x", pady=(4, 16))

    def open_groq(e=None):
        import webbrowser
        webbrowser.open("https://console.groq.com/keys")

    link.bind("<Button-1>", open_groq)
    link.bind("<Enter>", lambda e: link.config(fg=TEXT))
    link.bind("<Leave>", lambda e: link.config(fg=TEXT2))

    # ── Поле ввода ──
    entry_frame = tk.Frame(win, bg=BORDER, padx=1, pady=1)
    entry_frame.pack(padx=44, fill="x")

    entry = tk.Entry(
        entry_frame,
        font=("Segoe UI", 11),
        bg=BG2, fg=TEXT,
        insertbackground=TEXT,
        bd=0, relief="flat",
        highlightthickness=0,
    )
    entry.pack(fill="x", ipady=10, padx=1)

    # Подсветка рамки при фокусе
    def on_focus_in(e):
        entry_frame.config(bg=TEXT2)
    def on_focus_out(e):
        entry_frame.config(bg=BORDER)

    entry.bind("<FocusIn>",  on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    # ── Контекстное меню по ПКМ ──
    def paste_clipboard(event=None):
        try:
            text = win.clipboard_get()
            entry.delete(0, tk.END)
            entry.insert(0, text)
        except Exception:
            pass
        return "break"

    def show_context_menu(event):
        menu = tk.Menu(
            win, tearoff=0,
            bg=BG3, fg=TEXT,
            activebackground=BORDER,
            activeforeground=TEXT,
            bd=0, relief="flat",
            font=("Segoe UI", 10)
        )
        menu.add_command(label="  Paste", command=paste_clipboard)
        menu.add_command(label="  Clear", command=lambda: entry.delete(0, tk.END))
        menu.post(event.x_root, event.y_root)

    entry.bind("<Button-3>", show_context_menu)

    # ── Кнопка Launch ──
    btn = tk.Button(
        win, text="Launch",
        font=("Segoe UI", 11),
        bg=ACCENT, fg="#1c1c1c",
        bd=0, relief="flat", cursor="hand2",
        activebackground=ACCENT_HOVER,
        activeforeground="#1c1c1c",
        command=lambda: save_and_launch(entry.get(), win)
    )
    btn.pack(pady=24, ipadx=32, ipady=10)

    win.bind("<Return>", lambda e: save_and_launch(entry.get(), win))
    win.mainloop()

if __name__ == "__main__":
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            key = json.load(f).get("groq_api_key", "")
        if key:
            launch(key)
        else:
            show_setup()
    else:
        show_setup()
