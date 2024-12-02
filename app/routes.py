from flask import jsonify, request, render_template
from .models import Usuario, Consentimento, Termo
from app import db

def index():
    termos = Termo.query.all()
    return render_template('consent.html', termos=termos)

def portabilidade(usuario_id):
    usuario_atual = Usuario.query.get_or_404(usuario_id)
    dados = {
        "id": usuario_atual.id,
        "nome": usuario_atual.nome,
        "email": usuario_atual.email
    }
    return jsonify(dados)

def aceitar_consentimento():
    id_usuario = request.json.get('id_usuario')
    id_termo = request.json.get('id_termo')
    consentimento = Consentimento(id_usuario=id_usuario, id_termo=id_termo)
    db.session.add(consentimento)
    db.session.commit()
    return jsonify({"message": "Consentimento registrado."})

def revogar_consentimento():
    id_usuario = request.json.get('id_usuario')
    id_termo = request.json.get('id_termo')
    Consentimento.query.filter_by(id_usuario=id_usuario, id_termo=id_termo).delete()
    db.session.commit()
    return jsonify({"message": "Consentimento revogado."})

def criar_novo_termo():
    versao = request.json.get('versao')
    itens_obrigatorios = request.json.get('itens_obrigatorios')
    itens_opcionais = request.json.get('itens_opcionais', '')
    termo = Termo(versao=versao, itens_obrigatorios=itens_obrigatorios, itens_opcionais=itens_opcionais)
    db.session.add(termo)
    db.session.commit()
    return jsonify({"message": "Termo criado."})

def historico(usuario_id):
    consentimentos = Consentimento.query.filter_by(id_usuario=usuario_id).all()
    historico = [
        {"id_termo": c.id_termo, "data_aceite": c.data_aceite}
        for c in consentimentos
    ]
    return jsonify(historico)