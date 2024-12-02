from flask import jsonify
from .models import User

@app.route('/portabilidade/<int:usuario_id>', methods=['GET'])
def portabilidade(usuario_id):
    user = User.query.get_or_404(usuario_id)
    data = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
    return jsonify(data)

@app.route('/consentimento/aceitar', methods=['POST'])
def aceitar_consentimento():
    user_id = request.json.get('user_id')
    term_id = request.json.get('term_id')
    consent = Consent(user_id=user_id, term_id=term_id)
    db.session.add(consent)
    db.session.commit()
    return jsonify({"message": "Consentimento registrado."})

@app.route('/consentimento/revogar', methods=['POST'])
def revogar_consentimento():
    user_id = request.json.get('user_id')
    term_id = request.json.get('term_id')
    Consent.query.filter_by(user_id=user_id, term_id=term_id).delete()
    db.session.commit()
    return jsonify({"message": "Consentimento revogado."})

@app.route('/termos', methods=['POST'])
def criar_novo_termo():
    version = request.json.get('version')
    mandatory_items = request.json.get('mandatory_items')
    optional_items = request.json.get('optional_items', '')
    term = Term(version=version, mandatory_items=mandatory_items, optional_items=optional_items)
    db.session.add(term)
    db.session.commit()
    return jsonify({"message": "Term created."})

@app.route('/historico/<int:usuario_id>', methods=['GET'])
def historico(usuario_id):
    consents = Consent.query.filter_by(usuario_id=usuario_id).all()
    history = [
        {"term_id": c.term_id, "accepted_at": c.accepted_at}
        for c in consents
    ]
    return jsonify(history)