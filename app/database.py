from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base
from flask_sqlalchemy import SQLAlchemy
from config import Config
import pymysql

Base = declarative_base()

db = SQLAlchemy()

def criar_banco_de_dados_se_nao_existir(host, user, password, db_name):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        connection.commit()
        print(f"Banco de dados '{db_name}' verificado/criado.")
    finally:
        connection.close()

criar_banco_de_dados_se_nao_existir('localhost', 'root', 'root', 'db_name')
criar_banco_de_dados_se_nao_existir('localhost', 'root', 'root', 'banco2')