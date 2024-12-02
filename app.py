from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.database import engine1, engine2, Base
from app.models import *
from app.routes import portabilidade, aceitar_consentimento, revogar_consentimento, criar_novo_termo, historico, index

def criar_banco_de_dados():
    print("Criando tabelas no database 1...")
    Base.metadata.create_all(bind=engine1)
    print("Criando tabelas no database 2...")
    Base.metadata.create_all(bind=engine2)
    print("Databases criados com sucesso.")

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

app.add_url_rule('/', view_func=index, methods=['GET'])
app.add_url_rule('/portabilidade/<int:usuario_id>', view_func=portabilidade, methods=['GET'])
app.add_url_rule('/consentimento/aceitar', view_func=aceitar_consentimento, methods=['POST'])
app.add_url_rule('/consentimento/revogar', view_func=revogar_consentimento, methods=['POST'])
app.add_url_rule('/termos', view_func=criar_novo_termo, methods=['POST'])
app.add_url_rule('/historico/<int:usuario_id>', view_func=historico, methods=['GET'])

if __name__ == '__main__':
    criar_banco_de_dados()
    app.run(debug=True)
