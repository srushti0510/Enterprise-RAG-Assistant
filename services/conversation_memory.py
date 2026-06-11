import sqlite3
from datetime import datetime

DB_PATH = "conversation_memory.db"


def init_conversation_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            source TEXT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_conversation_turn(session_id: str, source: str, question: str, answer: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations (session_id, source, question, answer, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session_id,
        source,
        question,
        answer,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()


def get_recent_conversation(session_id: str, limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question, answer
        FROM conversations
        WHERE session_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (session_id, limit))

    rows = cursor.fetchall()
    conn.close()

    rows.reverse()

    memory = ""
    for question, answer in rows:
        memory += f"User: {question}\nAssistant: {answer}\n\n"

    return memory.strip()