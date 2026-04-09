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

def get_field_id(field_name):
    """Get field ID by name"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM fields WHERE field_name = ?", (field_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_or_get_person(person_name):
    """Add person if not exists, return person ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Try to get existing person
    cursor.execute("SELECT id FROM people WHERE name = ?", (person_name,))
    result = cursor.fetchone()
    
    if result:
        person_id = result[0]
    else:
        cursor.execute("INSERT INTO people (name) VALUES (?)", (person_name,))
        person_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return person_id

def add_contact_data(person_name, field_name, value):
    """Add or update contact data for a person"""
    person_id = add_or_get_person(person_name)
    field_id = get_field_id(field_name)
    
    if not field_id:
        return False, f"Field '{field_name}' does not exist. Create it with /addfield"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO contact_data (person_id, field_id, value) 
            VALUES (?, ?, ?)
            ON CONFLICT(person_id, field_id) 
            DO UPDATE SET value = ?
        ''', (person_id, field_id, value, value))
        conn.commit()
        return True, f"Added {field_name} = {value} for {person_name}"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def find_person(person_name):
    """Find all data for a person"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.name, f.field_name, cd.value
        FROM people p
        JOIN contact_data cd ON p.id = cd.person_id
        JOIN fields f ON cd.field_id = f.id
        WHERE p.name = ?
    ''', (person_name,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_people():
    """Return list of all people"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM people ORDER BY name")
    people = [row[0] for row in cursor.fetchall()]
    conn.close()
    return people

def delete_person(person_name):
    """Delete a person and all their data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM people WHERE name = ?", (person_name,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return False, f"Person '{person_name}' not found"
    
    person_id = result[0]
    cursor.execute("DELETE FROM contact_data WHERE person_id = ?", (person_id,))
    cursor.execute("DELETE FROM people WHERE id = ?", (person_id,))
    
    conn.commit()
    conn.close()
    return True, f"Deleted {person_name} and all their data"
