import sqlite3

def init_db():
    conn = sqlite3.connect('accreditations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accreditations (
        id INTEGER PRIMARY KEY,
        name TEXT,
        institute TEXT,
        acc_type TEXT,
        expiry_date TEXT
    )''')
    conn.commit()
    conn.close()

def add_accreditation(name, institute, acc_type, expiry_date):
    conn = sqlite3.connect('accreditations.db')
    c = conn.cursor()
    c.execute("INSERT INTO accreditations (name, institute, acc_type, expiry_date) VALUES (?, ?, ?, ?)",
              (name, institute, acc_type, expiry_date))
    conn.commit()
    conn.close()

def get_all_accreditations():
    conn = sqlite3.connect('accreditations.db')
    c = conn.cursor()
    c.execute("SELECT * FROM accreditations")
    rows = c.fetchall()
    conn.close()
    return rows
