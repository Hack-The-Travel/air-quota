# -*- coding: utf-8 -*-
import sqlite3


def db_execute(db_name, query):
    """Executes SQL query in sqlite database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows
