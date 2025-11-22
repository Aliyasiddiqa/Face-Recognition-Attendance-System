import sqlite3
from datetime import datetime

DB_NAME = "attendance.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_table(table="attendance"):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def mark_attendance(name, table="attendance"):
    create_table(table)
    conn = connect_db()
    cursor = conn.cursor()
    
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    
    cursor.execute(f"""
        INSERT INTO {table} (name, date, time)
        VALUES (?, ?, ?)
    """, (name, date, time))
    
    conn.commit()
    conn.close()
