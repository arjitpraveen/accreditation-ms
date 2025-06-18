import sqlite3

def init_accreditation_db():
    conn = sqlite3.connect('accreditation.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS accreditations (
            accreditation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            institution_id INTEGER,
            body_name TEXT,
            level TEXT,
            valid_from TEXT,
            valid_until TEXT,
            status TEXT,
            FOREIGN KEY (institution_id) REFERENCES institutions (institution_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_accreditation(institution_id, body_name, level, valid_from, valid_until, status):
    conn = sqlite3.connect('accreditation.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO accreditations (institution_id, body_name, level, valid_from, valid_until, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (institution_id, body_name, level, valid_from, valid_until, status))
    conn.commit()
    conn.close()

def get_all_accreditations():
    conn = sqlite3.connect('accreditation.db')
    c = conn.cursor()
    c.execute('SELECT * FROM accreditations')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_accreditation(accreditation_id):
    conn = sqlite3.connect('accreditation.db')
    c = conn.cursor()
    c.execute('DELETE FROM accreditations WHERE accreditation_id = ?', (accreditation_id,))
    conn.commit()
    conn.close()
