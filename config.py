import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/dev')

    SECRET_KEY = os.getenv("SECRET_KEY")