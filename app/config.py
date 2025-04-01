import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # If using SQLite and the URI starts with sqlite:///
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite:///'):
        # Ensure the directory exists
        db_path = SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True) 