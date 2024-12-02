from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import portabilidade, aceitar_consentimento, revogar_consentimento, criar_novo_termo, historico, index

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
    app.run(debug=True)