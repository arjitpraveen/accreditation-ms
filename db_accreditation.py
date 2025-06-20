import sqlite3
import datetime

# Renewal period mapping (years) for each accreditation body
RENEWAL_PERIODS = {
    "NAAC": 5,
    "NBA": 3,
    "AICTE": 1,
    "UGC": 5,
    "ISO": 3,
    "Other": 2
}

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

def init_renewal_db():
    conn = sqlite3.connect('accreditation.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS accreditation_renewals (
            renewal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            accreditation_id INTEGER,
            institution_id INTEGER,
            body_name TEXT,
            level TEXT,
            valid_from TEXT,
            valid_until TEXT,
            renewal_date TEXT,
            FOREIGN KEY (accreditation_id) REFERENCES accreditations (accreditation_id),
            FOREIGN KEY (institution_id) REFERENCES institutions (institution_id)
        )
    ''')
    conn.commit()
    conn.close()

def calculate_renewal_date(body_name, valid_until):
    period = RENEWAL_PERIODS.get(body_name, 2)  # default 2 years if not found
    dt = datetime.datetime.strptime(valid_until, "%Y-%m-%d")
    renewal_dt = dt + datetime.timedelta(days=1)
    return renewal_dt.strftime("%Y-%m-%d")

def add_renewal(accreditation_id, institution_id, body_name, level, valid_from, valid_until):
    renewal_date = calculate_renewal_date(body_name, valid_until)
    conn = sqlite3.connect('accreditation.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO accreditation_renewals (
            accreditation_id, institution_id, body_name, level, valid_from, valid_until, renewal_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (accreditation_id, institution_id, body_name, level, valid_from, valid_until, renewal_date))
    conn.commit()
    conn.close()

def get_all_renewals():
    conn = sqlite3.connect('accreditation.db')
    c = conn.cursor()
    c.execute('SELECT * FROM accreditation_renewals')
    rows = c.fetchall()
    conn.close()
    return rows
