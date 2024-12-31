# lib/config.py
import sqlite3

CONN = sqlite3.connect('company.db')
CONN.row_factory = sqlite3.Row
CURSOR = CONN.cursor()
