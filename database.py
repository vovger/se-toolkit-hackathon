import sqlite3

DB_PATH = "contacts.db"

def init_db():
    """Creates tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_name TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_data (
            person_id INTEGER,
            field_id INTEGER,
            value TEXT,
            FOREIGN KEY (person_id) REFERENCES people(id),
            FOREIGN KEY (field_id) REFERENCES fields(id),
            PRIMARY KEY (person_id, field_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_field(field_name):
    """Add a new custom field"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO fields (field_name) VALUES (?)", (field_name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_fields():
    """Return list of all fields"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT field_name FROM fields ORDER BY field_name")
    fields = [row[0] for row in cursor.fetchall()]
    conn.close()
    return fields
