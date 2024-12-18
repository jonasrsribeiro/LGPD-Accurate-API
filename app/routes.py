from http.client import HTTPException
from flask import app, jsonify, request, render_template, Blueprint

from app.notification import enviar_notificacoes_para_todos
from .models import Usuario, Consentimento, Termo
from .excluirUsarios import delete_users_based_on_historic
from app.models import Usuario, Termo, ItemTermo, Consentimento, HistoricoExclusao
from app.crud import (
    create_user, get_user, get_user_all, update_user, delete_user,
    create_term, get_term, get_term_all, update_term, delete_term,
    create_item_term, get_item_term, get_item_term_all, update_item_term, delete_item_term,
    create_consent, get_consent, get_consent_all, update_consent, delete_consent,
    create_historic_exclusion, get_historic_exclusion, get_historic_exclusion_all, verify_user_historic_exclusion,
    get_user_by_email_password, solicitar_token, portabilidade)

bp = Blueprint('routes', __name__)

# USERS
@bp.route('/solicitar-token/<int:user_id>', methods=['GET'])
def rota_solicitar_token(user_id: int):
    return solicitar_token(user_id)

@bp.route('/portabilidade/<int:user_id>', methods=['GET'])
def rota_portabilidade(user_id: int):
    return portabilidade(user_id)

@bp.route("/dashboard/", methods=["GET", "POST"])
def dashboard():
    termos = Termo.query.all()
    termos_agrupados = []
    for termo in termos:
        itens = [
            {
                "id": item.id,
                "descricao": item.descricao,
                "obrigatorio": item.obrigatorio,
            }
            for item in termo.itens
        ]
        termos_agrupados.append(
            {
                "id": termo.id,
                "versao": termo.versao,
                "atual": termo.atual,
                "data_criacao": termo.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
                "itens": itens,
            }
        )
    return render_template('consent.html', termos=termos_agrupados)

@bp.route("/login/", methods=["GET","POST"])
def login():
    return render_template('login.html')

@bp.route('/logar/', methods=['POST'])
def logar():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    
    usuario = Usuario.query.filter_by(email=email, senha=senha, ativo=True).first()
    
    if usuario:
        veriify = verify_user_historic_exclusion(usuario.id)
        if veriify:
            return jsonify({"message": "Usuario nao existe"})
        return jsonify({"message": "Login bem-sucedido", "user": usuario.to_dict()})
    else:
        return jsonify({"message": "Usuario ou senha invalidos"}), 401


@bp.route("/usuarios/", methods=["POST"])
def create_user_route():
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    senha = data['senha']
    print("Nome: ", nome)
    return jsonify(create_user(nome, email, senha))

@bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
def get_user_route(usuario_id: int):
    user = get_user(usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return jsonify(user)

@bp.route("/usuarios/", methods=["GET"])
def get_all_users_route():
    return jsonify(get_user_all())

@bp.route("/usuarios/<int:usuario_id>",methods=["PUT"])
def update_user_route(usuario_id: int):
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    senha = data['senha']
    ativo = bool(data["ativo"])

    user = update_user(usuario_id, nome, email, senha, ativo)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return jsonify(user)

@bp.route("/usuarios/deletar/<int:usuario_id>", methods=["DELETE"])
def delete_user_route(usuario_id: int):
    user = delete_user(usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return jsonify({"message": "Usuário excluído com sucesso", "usuario": user})


## TERMOS

@bp.route("/termos/", methods=["POST"])
def create_term_route():
    data = request.get_json()
    versao = data["versao"]
    atual = data["atual"]
    return jsonify(create_term(versao, atual))

@bp.route("/termos/<int:termo_id>", methods=["GET"])
def get_term_route(termo_id: int):
    term = get_term(termo_id)
    if not term:
        raise HTTPException(status_code=404, detail="Termo não encontrado")
    return jsonify(term)

@bp.route("/termos/",methods=["GET"])
def get_all_terms_route():
    return jsonify(get_term_all())

@bp.route("/termos/<int:termo_id>", methods=["PUT"])
def update_term_route(termo_id: int):
    data = request.get_json()
    versao = data["versao"]
    atual = data["atual" ]   
    term = update_term(termo_id, versao, atual)
    if not term:
        raise HTTPException(status_code=404, detail="Termo não encontrado")
    return jsonify(term)

@bp.route("/termos/<int:termo_id>", methods=["DELETE"])
def delete_term_route(termo_id: int):
    term = delete_term(termo_id)
    if not term:
        raise HTTPException(status_code=404, detail="Termo não encontrado")
    return jsonify({"message": "Termo excluído com sucesso", "termo": term})

# ITEMS DOS TERMOS

@bp.route("/termos/items/", methods=["POST"])
def create_item_term_route():
    data = request.get_json()
    id_termo = data["id_termo"]
    descricao = data["descricao"]
    obrigatorio = data["obrigatorio"]
    return jsonify(create_item_term(id_termo, descricao, obrigatorio))

@bp.route("/termos/items/<int:item_termo_id>")
def get_item_term_route(item_termo_id: int):
    item = get_item_term(item_termo_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item do termo não encontrado")
    return jsonify(item)

@bp.route("/termos/items/", methods=["GET"])
def get_all_items_term_route():
    return jsonify(get_item_term_all())

@bp.route("/termos/items/<int:item_termo_id>", methods=["PUT"])
def update_item_term_route(item_termo_id: int):
    data = request.get_json()
    descricao = data["descricao"]
    id_termo = int(data["id_termo"])
    obrigatorio = bool(data["obrigatorio"])
    item = update_item_term(item_termo_id, id_termo, descricao, obrigatorio)
    if not item:
        raise HTTPException(status_code=404, detail="Item do termo não encontrado")
    return jsonify(item)

@bp.route("/termos/items/<int:item_termo_id>", methods=["DELETE"])
def delete_item_term_route(item_termo_id: int):
    item = delete_item_term(item_termo_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item do termo não encontrado")
    return jsonify({"message": "Item do termo excluído com sucesso", "item_termo": item})

# Consentimento

@bp.route("/consent/", methods=["POST"])
def create_consent_route():
    data = request.get_json()
    id_usuario = int(data["usuario"]["id_usuario"])
    response = []

    for item in data["itens"]:
        id_item_termo = int(item["id_item_termo"])
        aceite_recusa = bool(item["aceite_recusa"])
        result = create_consent(id_usuario, id_item_termo, aceite_recusa)
        response.append(result)

    return jsonify(response)

@bp.route("/consentimento/<int:consentimento_id>", methods=["GET"])
def get_consent_route(consentimento_id: int):
    consent = get_consent(consentimento_id)
    if not consent:
        raise HTTPException(status_code=404, detail="Consentimento não encontrado")
    return jsonify(consent)

@bp.route("/consentimento/", methods=["GET"])
def get_all_consents_route():
    return jsonify(get_consent_all())

@bp.route("/consentimento/<int:consentimento_id>", methods=["PUT"])
def update_consent_route(consentimento_id: int, id_usuario: int, id_item_termo: int, aceite_recusa: bool):
    data = request.get_json()
    id_usuario = int(data["id_usuario"])
    id_item_termo = int(data["id_item_termo"])
    aceite_recusa = bool(data["aceite_recusa"])
    consent = update_consent(consentimento_id, id_usuario, id_item_termo, aceite_recusa)
    if not consent:
        raise HTTPException(status_code=404, detail="Consentimento não encontrado")
    return jsonify(consent)

@bp.route("/consentimento/<int:consentimento_id>", methods=["DELETE"])
def delete_consent_route(consentimento_id: int):
    consent = delete_consent(consentimento_id)
    if not consent:
        raise HTTPException(status_code=404, detail="Consentimento não encontrado")
    return jsonify({"message": "Consentimento excluído com sucesso", "consentimento": consent})

## HISTORICO DE EXCLUSAO

@bp.route("/historico/exclusao/", methods=["GET"])
def get_all_historic_exclusion_route():
    return jsonify(get_historic_exclusion_all())

@bp.route("/historico/exclusao/<int:historico_exclusao_id>", methods=["GET"])
def get_historic_exclusion_route(historico_exclusao_id: int):
    historic = get_historic_exclusion(historico_exclusao_id)
    if not historic:
        raise HTTPException(status_code=404, detail="Histórico de exclusão não encontrado")
    return jsonify(historic)

@bp.route("/historico/exclusao/todos", methods=["DELETE"])
def delete_all_users_based_on_historic():
    ids = delete_users_based_on_historic()
    return jsonify({"message": "Usuários excluídos com base no histórico", "ids": ids})

@bp.route("/notificar_usuarios", methods=["POST"])
def notificar_usuarios():
    emails_enviados = enviar_notificacoes_para_todos()
    return jsonify({"message": "Notificações enviadas com sucesso!", "emails": emails_enviados})

@bp.route("/panico", methods=["GET"])
def emergency_page():
    return render_template("notification.html")