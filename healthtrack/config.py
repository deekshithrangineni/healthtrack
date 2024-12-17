import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database
DATABASE_PATH = os.path.join(BASE_DIR, 'backend', 'healthtrack.db')

# Uploads
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads', 'medical_records')

# Security
SECRET_KEY = 'your-secret-key-here'  # Change this in production
SESSION_DURATION = 3600  # 1 hour in seconds

# File upload settings
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size