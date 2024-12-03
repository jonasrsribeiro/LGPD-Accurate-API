from flask import Flask
from app.database import db
from app.models import *
from app.__init__ import create_app
from app.excluirUsarios import delete_users_based_on_historic  

def criar_banco_de_dados():
    with app.app_context():
        print("Criando tabelas no database...")
        db.create_all()
        engine_db2 = db.get_engine(app, bind='db2')
        db.metadata.create_all(bind=engine_db2)
        print("Databases criados com sucesso!")
        print("Excluindo usuários baseado no histórico de exclusão...")
        delete_users_based_on_historic()


app = create_app()

if __name__ == '__main__':
    criar_banco_de_dados()
    app.run(debug=True)