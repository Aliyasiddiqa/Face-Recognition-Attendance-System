import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from detector import register_face, start_recognition
from train import train_model

DB_NAME = "attendance.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER,
            name TEXT,
            datetime TEXT,
            FOREIGN KEY(id) REFERENCES people(id)
        )
    """)

    conn.commit()
    conn.close()

def register_action():
    user_id = entry_id.get().strip()
    name = entry_name.get().strip()

    if not user_id.isdigit() or not name:
        messagebox.showerror("Input error", "ID must be numeric and name must not be empty.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO people (id, name) VALUES (?, ?)", (int(user_id), name))
    conn.commit()
    conn.close()

    register_face(int(user_id), name)
    messagebox.showinfo("Done", f"Captured samples for {name} (ID: {user_id}).")

def train_action():
    train_model()
    messagebox.showinfo("Training", "Training completed. Created trainer.yml")

def start_action():
    start_recognition()

root = tk.Tk()
root.title("Face Recognition Attendance (A2)")

frm = tk.Frame(root, padx=10, pady=10)
frm.pack()

tk.Label(frm, text="Numeric ID:").grid(row=0, column=0, sticky="e")
entry_id = tk.Entry(frm)
entry_id.grid(row=0, column=1)

tk.Label(frm, text="Name:").grid(row=1, column=0, sticky="e")
entry_name = tk.Entry(frm)
entry_name.grid(row=1, column=1)

btn_register = tk.Button(frm, text="Register", command=register_action, width=20)
btn_register.grid(row=2, column=0, columnspan=2, pady=6)

btn_train = tk.Button(frm, text="Train Model", command=train_action, width=20)
btn_train.grid(row=3, column=0, columnspan=2, pady=6)

btn_start = tk.Button(frm, text="Start Attendance", command=start_action, width=20, bg="#4CAF50", fg="white")
btn_start.grid(row=4, column=0, columnspan=2, pady=6)

lbl = tk.Label(frm, text="Notes:\n- Make sure webcam is accessible.\n- Install opencv-contrib-python.\n- Register users before training.", justify="left")
lbl.grid(row=5, column=0, columnspan=2, pady=6)

connect_db()
root.mainloop()
