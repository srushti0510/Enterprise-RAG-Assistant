import sqlite3
from datetime import datetime

DB_NAME = "feedback.db"


def init_feedback_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            feedback TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_feedback(question: str, answer: str, feedback: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (question, answer, feedback, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        question,
        answer,
        feedback,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()