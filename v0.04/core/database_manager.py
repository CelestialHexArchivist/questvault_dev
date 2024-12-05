import sqlite3

def initialize_database(db_name):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS domains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()

def get_all_items(db_name):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, description, category FROM items')
        return cursor.fetchall()

def search_items_by_keyword(db_name, keyword):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, description, category 
            FROM items 
            WHERE name LIKE ? OR description LIKE ? OR category LIKE ?
        ''', (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        return cursor.fetchall()

def search_items_by_category(db_name, category):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, description, category FROM items WHERE category = ?', (category,))
        return cursor.fetchall()
