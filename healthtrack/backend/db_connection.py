# backend/db_connection.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('health_track.db')
    conn.row_factory = sqlite3.Row
    return conn