import sqlite3
import pandas as pd

DB_NAME = "feedback.db"


def get_feedback_summary():
    conn = sqlite3.connect(DB_NAME)

    total = pd.read_sql(
        "SELECT COUNT(*) as total FROM feedback",
        conn
    ).iloc[0]["total"]

    helpful = pd.read_sql(
        "SELECT COUNT(*) as helpful FROM feedback WHERE feedback='Helpful'",
        conn
    ).iloc[0]["helpful"]

    not_helpful = pd.read_sql(
        "SELECT COUNT(*) as not_helpful FROM feedback WHERE feedback='Not Helpful'",
        conn
    ).iloc[0]["not_helpful"]

    recent = pd.read_sql(
        """
        SELECT question, feedback, timestamp
        FROM feedback
        ORDER BY id DESC
        LIMIT 10
        """,
        conn
    )

    conn.close()

    return {
        "total": total,
        "helpful": helpful,
        "not_helpful": not_helpful,
        "recent": recent
    }