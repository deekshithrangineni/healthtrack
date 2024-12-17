import os
import secrets
import re
from datetime import datetime
from PIL import Image

class Security:
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    @staticmethod
    def generate_session_token():
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def is_allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Security.ALLOWED_EXTENSIONS
    
    @staticmethod
    def verify_file_size(file_size):
        """Verify file size is within limits"""
        return file_size <= Security.MAX_FILE_SIZE
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize the filename"""
        # Remove any directory components
        filename = os.path.basename(filename)
        # Remove any non-alphanumeric characters except periods and hyphens
        filename = re.sub(r'[^a-zA-Z0-9.-]', '_', filename)
        return filename
    
    @staticmethod
    def save_file_securely(uploaded_file, user_id):
        """Save uploaded file securely"""
        try:
            # Create user-specific upload directory
            upload_dir = os.path.join('uploads', 'medical_records', str(user_id))
            os.makedirs(upload_dir, exist_ok=True)
            
            # Check file size
            if not Security.verify_file_size(uploaded_file.size):
                raise ValueError("File too large")
            
            # Verify file extension
            if not Security.is_allowed_file(uploaded_file.name):
                raise ValueError("Invalid file type")
            
            # Sanitize and secure filename
            original_filename = Security.sanitize_filename(uploaded_file.name)
            file_ext = os.path.splitext(original_filename)[1].lower()
            secure_filename = f"{secrets.token_hex(16)}{file_ext}"
            file_path = os.path.join(upload_dir, secure_filename)
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            return secure_filename, original_filename
            
        except Exception as e:
            # If anything goes wrong, ensure we don't leave partial files
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            raise e
    
    @staticmethod
    def get_file_path(user_id, filename):
        """Get secure file path"""
        sanitized_filename = Security.sanitize_filename(filename)
        file_path = os.path.join('uploads', 'medical_records', 
                                str(user_id), sanitized_filename)
        
        # Verify path is within uploads directory
        abs_path = os.path.abspath(file_path)
        uploads_dir = os.path.abspath('uploads')
        if not abs_path.startswith(uploads_dir):
            raise ValueError("Invalid file path")
        
        return file_path