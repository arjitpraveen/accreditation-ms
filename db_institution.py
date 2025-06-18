import sqlite3

def init_institution_db():
    conn = sqlite3.connect('institution.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS institutions (
            institution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT,
            location TEXT,
            contact_email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_institution(name, type_, location, contact_email):
    conn = sqlite3.connect('institution.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO institutions (name, type, location, contact_email)
        VALUES (?, ?, ?, ?)
    ''', (name, type_, location, contact_email))
    conn.commit()
    conn.close()

def get_all_institutions():
    conn = sqlite3.connect('institution.db')
    c = conn.cursor()
    c.execute('SELECT * FROM institutions')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_institution(institution_id):
    conn = sqlite3.connect('institution.db')
    c = conn.cursor()
    c.execute('DELETE FROM institutions WHERE institution_id = ?', (institution_id,))
    conn.commit()
    conn.close()
