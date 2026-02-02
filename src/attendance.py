import sqlite3
from datetime import datetime

DB = "data/attendance.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            user TEXT,
            date TEXT,
            punch_in TEXT,
            punch_out TEXT
        )
    """)
    conn.commit()
    conn.close()

def mark_attendance(user):
    today = datetime.now().date().isoformat()
    time_now = datetime.now().strftime("%H:%M:%S")

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM attendance WHERE user=? AND date=?", (user, today))
    row = c.fetchone()

    if row is None:
        c.execute(
            "INSERT INTO attendance VALUES (?, ?, ?, ?)",
            (user, today, time_now, None),
        )
        action = "PUNCH-IN"
    elif row[3] is None:
        c.execute(
            "UPDATE attendance SET punch_out=? WHERE user=? AND date=?",
            (time_now, user, today),
        )
        action = "PUNCH-OUT"
    else:
        action = "ALREADY MARKED"

    conn.commit()
    conn.close()
    return action
