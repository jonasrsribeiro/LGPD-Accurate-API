import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_URI', 'mysql+pymysql://user:password@localhost/db_name')
    SQLALCHEMY_DATABASE_URI_2 = os.getenv('MYSQL_URI_2','mysql+pymysql://user:senha@localhost:3306/banco2')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')