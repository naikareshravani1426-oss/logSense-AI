import sqlite3
import json
from datetime import datetime

DB_PATH = 'logs.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                raw_log TEXT,
                domain TEXT,
                severity TEXT,
                result TEXT,
                timestamp TEXT
            )
        ''')

def save_log(raw_log: str, result: dict):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        domain = result.get('domain')
        severity = result.get('severity')
        result_json = json.dumps(result)
        timestamp = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO logs (raw_log, domain, severity, result, timestamp) VALUES (?, ?, ?, ?, ?)",
            (raw_log, domain, severity, result_json, timestamp)
        )
        conn.commit()
        return cursor.lastrowid

def get_history(limit: int = 20):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, domain, severity, timestamp FROM logs ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_log_by_id(log_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT raw_log, result FROM logs WHERE id = ?",
            (log_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        parsed_json_dict = json.loads(row['result'])
        return {
            'raw_log': row['raw_log'],
            'result': parsed_json_dict
        }
