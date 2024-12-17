import hashlib
import secrets
from datetime import datetime
from .db_connection import get_db_connection
import sqlite3

class Auth:
    @staticmethod
    def hash_password(password, salt=None):
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        
        return password_hash, salt

    @staticmethod
    def register_user(email, password, name):
        """Register a new user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if email already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone() is not None:
                return False, "Email already registered"
            
            # Hash password with salt
            password_hash, salt = Auth.hash_password(password)
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (email, password_hash, salt, name)
                VALUES (?, ?, ?, ?)
            ''', (email, password_hash, salt, name))
            
            conn.commit()
            return True, "Registration successful"
            
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def login_user(email, password):
        """Authenticate user"""
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, password_hash, salt, name
                FROM users
                WHERE email = ?
            ''', (email,))
            
            user = cursor.fetchone()
            if not user:
                return None, "Invalid email or password"
            
            # Verify password
            password_hash, _ = Auth.hash_password(password, user['salt'])
            if password_hash == user['password_hash']:
                return {
                    'id': user['id'],
                    'email': email,
                    'name': user['name']
                }, "Login successful"
            
            return None, "Invalid email or password"
        except Exception as e:
            return None, f"Error: {e}"
        finally:
            conn.close()
            
  