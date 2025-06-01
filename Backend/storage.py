import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("data/dreams.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS dreams (
            id INTEGER PRIMARY KEY,
            prompt TEXT,
            transcription TEXT,
            image_url TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_dream(prompt, transcription, image_url):
    conn = sqlite3.connect("data/dreams.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO dreams (prompt, transcription, image_url, created_at)
        VALUES (?, ?, ?, ?)
    ''', (prompt, transcription, image_url, datetime.now().isoformat()))
    conn.commit()
    conn.close()