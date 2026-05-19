import os, sys, json, threading, time, tkinter as tk, webbrowser
from tkinter import messagebox

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".echo-agent", "config.json")
BASE_DIR = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))  # ✅ __file__

def start_flask(api_key):
    os.environ["GROQ_API_KEY"] = api_key
    import app as flask_app
    flask_app.app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def save_and_launch(key, win):
    k = key.strip()
    if not k.startswith("gsk_"):
        messagebox.showerror("Error", "Key must start with gsk_")
        return
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"groq_api_key": k}, f)
    win.destroy()
    launch(k)

def launch(api_key):
    import socket
    t = threading.Thread(target=start_flask, args=(api_key,), daemon=True)
    t.start()
    for _ in range(30):
        time.sleep(0.3)
        try:
            s = socket.create_connection(("127.0.0.1", 5000), timeout=0.5)
            s.close()
            break
        except: continue
    webbrowser.open("http://127.0.0.1:5000")  # ✅ браузер вместо pywebview

def show_setup():
    win = tk.Tk()
    win.title("Echo — Setup")
    win.geometry("520x340")
    win.configure(bg="#0e0e10")
    win.resizable(False, False)
    
    tk.Label(win, text="⬡ Echo", font=("Segoe UI", 26, "bold"), bg="#0e0e10", fg="#a78bfa").pack(pady=18)
    tk.Label(win, text="1. Go to console.groq.com\n2. Create API Key\n3. Paste below:", bg="#0e0e10", fg="#d4d4d8").pack()
    
    entry = tk.Entry(win, font=("Segoe UI", 11), bg="#18181b", fg="#d4d4d8", insertbackground="#a78bfa")
    entry.pack(pady=10, ipady=8, padx=30, fill="x")
    
    tk.Button(win, text="Launch →", bg="#7c3aed", fg="white", font=("Segoe UI", 12, "bold"),
              command=lambda: save_and_launch(entry.get(), win)).pack(pady=20, ipadx=20, ipady=8)
    
    win.bind("<Return>", lambda e: save_and_launch(entry.get(), win))
    win.mainloop()

if __name__ == "__main__":  # ✅ __name__
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            key = json.load(f).get("groq_api_key", "")
        launch(key) if key else show_setup()
    else:
        show_setup()
