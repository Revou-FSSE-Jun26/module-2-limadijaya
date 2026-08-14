import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
    
    # Connection String Format: postgresql://username:password@localhost:5432/database_name
    # Replace 'postgres:postgres' with your local PostgreSQL user and password.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:Lolihai88$@localhost/revoshop_db' 
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False