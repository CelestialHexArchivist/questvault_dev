import sqlite3

DB_NAME = "subnautica_items.db"

def add_domain(url):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO domains (url) VALUES (?)', (url,))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Domain already exists: {url}")

def delete_domain(url):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM domains WHERE url = ?', (url,))
        conn.commit()

def get_domains():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT url FROM domains')
        return [row[0] for row in cursor.fetchall()]
