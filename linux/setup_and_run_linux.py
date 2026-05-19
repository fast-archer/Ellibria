#!/usr/bin/env python3
import os, sys, json, threading, time, subprocess, webbrowser, tkinter as tk
from tkinter import messagebox

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".echo-agent", "config.json")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def start_flask(api_key):
    os.environ["GROQ_API_KEY"] = api_key
    sys.path.insert(0, BASE_DIR)
    import app as flask_app
    flask_app.app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def open_browser():
    import socket
    for _ in range(20):
        time.sleep(0.5)
        try:
            s = socket.create_connection(("127.0.0.1", 5000), timeout=1)
            s.close()
            break
        except OSError:
            continue
    # xdg-open надёжнее чем webbrowser на Arch
    try:
        subprocess.Popen(["xdg-open", "http://127.0.0.1:5000"])
    except Exception:
        webbrowser.open("http://127.0.0.1:5000")

def launch(api_key):
    t = threading.Thread(target=start_flask, args=(api_key,), daemon=True)
    t.start()
    threading.Thread(target=open_browser, daemon=True).start()
    # Держим процесс живым молча
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEcho stopped.")

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

def show_setup():
    win = tk.Tk()
    win.title("Echo — Setup")
    win.geometry("520x300")
    win.configure(bg="#0e0e10")
    win.resizable(False, False)

    tk.Label(win, text="⬡ Echo", font=("Sans", 24, "bold"),
             bg="#0e0e10", fg="#a78bfa").pack(pady=16)
    tk.Label(win, text="1. Go to console.groq.com",
             bg="#0e0e10", fg="#d4d4d8", font=("Sans", 11)).pack()
    tk.Label(win, text="2. Sign up → API Keys → Create key",
             bg="#0e0e10", fg="#d4d4d8", font=("Sans", 11)).pack(pady=2)
    tk.Label(win, text="3. Paste your key below:",
             bg="#0e0e10", fg="#d4d4d8", font=("Sans", 11)).pack(pady=(10,4))

    frame = tk.Frame(win, bg="#0e0e10")
    frame.pack(padx=30, fill="x")

    entry = tk.Entry(frame, font=("Sans", 11),
                     bg="#18181b", fg="#d4d4d8",
                     insertbackground="#a78bfa", bd=0, relief="flat",
                     highlightthickness=1, highlightbackground="#3f3f46",
                     highlightcolor="#7c3aed")
    entry.pack(fill="x", ipady=9, padx=1, pady=1)

    def paste(event=None):
        try:
            text = win.clipboard_get()
            entry.delete(0, tk.END)
            entry.insert(0, text)
        except Exception:
            pass
        return "break"

    entry.bind("<Control-v>", paste)
    entry.bind("<Control-V>", paste)
    entry.bind("<Control-KeyPress>", lambda e: paste() if e.keycode == 86 else None)

    def show_menu(event):
        menu = tk.Menu(win, tearoff=0, bg="#18181b", fg="#d4d4d8",
                       activebackground="#7c3aed", activeforeground="white")
        menu.add_command(label="Paste", command=paste)
        menu.add_command(label="Clear", command=lambda: entry.delete(0, tk.END))
        menu.post(event.x_root, event.y_root)
    entry.bind("<Button-3>", show_menu)

    tk.Button(win, text="Launch →",
              font=("Sans", 12, "bold"),
              bg="#7c3aed", fg="white", bd=0, cursor="hand2",
              activebackground="#6d28d9",
              command=lambda: save_and_launch(entry.get(), win)
              ).pack(pady=20, ipadx=24, ipady=10)

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
