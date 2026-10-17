"""
Database connection and session management module.
Supports SQLite by default and external SQL databases (MySQL, PostgreSQL).
"""

import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cricbuzz.db")

def get_connection():
    """Returns a SQLite connection object."""
    conn = sqlite3.connect(DEFAULT_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
