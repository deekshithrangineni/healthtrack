

# backend/validators.py
import re
from datetime import datetime

class Validators:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        return True, "Password is strong"

    @staticmethod
    def validate_vital_signs(vitals):
        """Validate vital signs data"""
        validations = {
            'blood_pressure_sys': lambda x: 70 <= x <= 200,
            'blood_pressure_dia': lambda x: 40 <= x <= 130,
            'heart_rate': lambda x: 40 <= x <= 200,
            'temperature': lambda x: 95.0 <= x <= 105.0,
            'weight': lambda x: 50 <= x <= 500,
            'oxygen': lambda x: 50 <= x <= 100
        }
        
        for field, validator in validations.items():
            if field not in vitals or not validator(vitals[field]):
                return False, f"Invalid {field.replace('_', ' ')}"
        
        return True, "Valid vital signs"

    @staticmethod
    def validate_date(date_str):
        """Validate date string format"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False