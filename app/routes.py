from flask import jsonify
from .models import User

@app.route('/portability/<int:user_id>', methods=['GET'])
def portability(user_id):
    user = User.query.get_or_404(user_id)
    data = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
    return jsonify(data)

@app.route('/consent/accept', methods=['POST'])
def accept_consent():
    user_id = request.json.get('user_id')
    term_id = request.json.get('term_id')
    consent = Consent(user_id=user_id, term_id=term_id)
    db.session.add(consent)
    db.session.commit()
    return jsonify({"message": "Consent registered."})

@app.route('/consent/revoke', methods=['POST'])
def revoke_consent():
    user_id = request.json.get('user_id')
    term_id = request.json.get('term_id')
    Consent.query.filter_by(user_id=user_id, term_id=term_id).delete()
    db.session.commit()
    return jsonify({"message": "Consent revoked."})

@app.route('/terms', methods=['POST'])
def create_term():
    version = request.json.get('version')
    mandatory_items = request.json.get('mandatory_items')
    optional_items = request.json.get('optional_items', '')
    term = Term(version=version, mandatory_items=mandatory_items, optional_items=optional_items)
    db.session.add(term)
    db.session.commit()
    return jsonify({"message": "Term created."})

@app.route('/history/<int:user_id>', methods=['GET'])
def history(user_id):
    consents = Consent.query.filter_by(user_id=user_id).all()
    history = [
        {"term_id": c.term_id, "accepted_at": c.accepted_at}
        for c in consents
    ]
    return jsonify(history)