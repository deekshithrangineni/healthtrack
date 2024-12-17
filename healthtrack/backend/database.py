from datetime import datetime
from .db_connection import get_db_connection

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create all tables
    cursor.executescript('''
        -- Users table
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            name TEXT NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Vital signs tracking
        CREATE TABLE IF NOT EXISTS vital_signs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            blood_pressure_sys INTEGER NOT NULL,
            blood_pressure_dia INTEGER NOT NULL,
            heart_rate INTEGER NOT NULL,
            weight REAL,
            status TEXT,
            date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        -- Medical records
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            record_type TEXT NOT NULL,
            status TEXT DEFAULT 'Encrypted',
            shared_with TEXT,
            record_date DATE NOT NULL,
            file_path TEXT,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        -- Medications
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            frequency TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE,
            notes TEXT,
            active BOOLEAN DEFAULT 1,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        -- Appointments
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            provider TEXT NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            location TEXT,
            notes TEXT,
            status TEXT DEFAULT 'Scheduled',
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')

    # Add sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Add sample user
        cursor.execute('''
            INSERT INTO users (email, password_hash, salt, name)
            VALUES (?, ?, ?, ?)
        ''', ('demo@healthtrack.com', 'sample_hash', 'sample_salt', 'John Doe'))
        
        user_id = cursor.lastrowid

        # Add sample vital signs
        cursor.execute('''
            INSERT INTO vital_signs (
                user_id, blood_pressure_sys, blood_pressure_dia,
                heart_rate, weight, status
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, 120, 80, 72, 165, 'Normal'))

        # Add sample records
        cursor.execute('''
            INSERT INTO medical_records (
                user_id, title, record_type, record_date
            ) VALUES (?, ?, ?, ?)
        ''', (user_id, "Lab Results - March 1, 2024", "Labs", "2024-03-01"))

    conn.commit()
    conn.close()

__all__ = ['init_db']