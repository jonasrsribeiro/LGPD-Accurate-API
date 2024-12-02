from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config
import pymysql

Base = declarative_base()

def criar_banco_de_dados_se_nao_existir(engine_url, db_name):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root'
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        connection.commit()
        print(f"Banco de dados '{db_name}' verificado/criado.")
    finally:
        connection.close()

# Cria os bancos de dados, se necessário
criar_banco_de_dados_se_nao_existir('mysql+pymysql://root:root@localhost:3306', 'db_name')
criar_banco_de_dados_se_nao_existir('mysql+pymysql://root:root@localhost:3306', 'banco2')

# Cria os engines
engine1 = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
engine2 = create_engine(Config.SQLALCHEMY_DATABASE_URI_2, echo=True)

SessionLocal1 = sessionmaker(autocommit=False, autoflush=False, bind=engine1)
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)

def get_db1():
    db = SessionLocal1()
    try:
        yield db
    finally:
        db.close()

def get_db2():
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()