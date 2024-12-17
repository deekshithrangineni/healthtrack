# backend/models.py
from datetime import datetime
from backend.db_connection import get_db_connection

class HealthData:
    @staticmethod
    def get_vital_signs(user_id, limit=7):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM vital_signs
                WHERE user_id = ?
                ORDER BY date_recorded DESC
                LIMIT ?
            ''', (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def add_vital_signs(user_id, data):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO vital_signs (
                    user_id, blood_pressure_sys, blood_pressure_dia,
                    heart_rate, weight, status
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                data['blood_pressure_sys'],
                data['blood_pressure_dia'],
                data['heart_rate'],
                data['weight'],
                data.get('status', 'Normal')
            ))
            conn.commit()
            return True, "Vital signs recorded successfully"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def get_medical_records(user_id, record_type=None, limit=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Build the query based on parameters
            query = 'SELECT * FROM medical_records WHERE user_id = ?'
            params = [user_id]
            
            if record_type and record_type != "All":
                query += ' AND record_type = ?'
                params.append(record_type)
                
            query += ' ORDER BY record_date DESC'
            
            if limit:
                query += ' LIMIT ?'
                params.append(limit)
                
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_medications(user_id, active_only=True, limit=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = 'SELECT * FROM medications WHERE user_id = ?'
            params = [user_id]
            
            if active_only:
                query += ' AND active = 1'
                
            query += ' ORDER BY date_created DESC'
            
            if limit:
                query += ' LIMIT ?'
                params.append(limit)
                
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_appointments(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM appointments
                WHERE user_id = ? AND appointment_date >= DATE('now')
                ORDER BY appointment_date, appointment_time
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_user_profile(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            return dict(cursor.fetchone())
        finally:
            conn.close()

    @staticmethod
    def update_user_profile(user_id, name, email, dob, gender, height, blood_type):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE users 
                SET name = ?, email = ?, dob = ?, gender = ?, 
                    height = ?, blood_type = ?
                WHERE id = ?
            ''', (name, email, dob, gender, height, blood_type, user_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()