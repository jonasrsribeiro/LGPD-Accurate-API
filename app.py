from flask import Flask
from app.database import db
from app.models import *
from app.__init__ import create_app
from app.routes import portabilidade, aceitar_consentimento, revogar_consentimento, criar_novo_termo, historico, index

def criar_banco_de_dados():
    with app.app_context():
        print("Criando tabelas no database 1...")
        db.create_all()
        print("Criando tabelas no database 2...")
        engine_db2 = db.get_engine(app, bind='db2')
        db.metadata.create_all(bind=engine_db2)
        print("Databases criados com sucesso!")

app = create_app()

# Definição de rotas
app.add_url_rule('/', view_func=index, methods=['GET'])
app.add_url_rule('/portabilidade/<int:usuario_id>', view_func=portabilidade, methods=['GET'])
app.add_url_rule('/consentimento/aceitar', view_func=aceitar_consentimento, methods=['POST'])
app.add_url_rule('/consentimento/revogar', view_func=revogar_consentimento, methods=['POST'])
app.add_url_rule('/termos', view_func=criar_novo_termo, methods=['POST'])
app.add_url_rule('/historico/<int:usuario_id>', view_func=historico, methods=['GET'])

if __name__ == '__main__':
    criar_banco_de_dados()
    app.run(debug=True)