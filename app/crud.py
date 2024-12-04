from app.models import Usuario, Termo, Consentimento, HistoricoExclusao, ItemTermo
from .database import db
from datetime import datetime

def create_user(nome: str, email: str, senha: str):
    try:
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        print("novo_usuario: ", novo_usuario)
        db.session.add(novo_usuario)
        db.session.commit()
        db.session.refresh(novo_usuario)
        return novo_usuario.to_dict()
    except Exception as e:
        db.session.rollback()
        print("Erro ao criar usuário:", e)
        return None

def get_user(usuario_id: int, usage=False):
    usuario =  db.session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usage:
        return usuario
    return usuario.to_dict()

def get_user_all():
    usuarios = db.session.query(Usuario).all()
    return [usuario.to_dict() for usuario in usuarios]


def update_user(usuario_id: int, nome: str, email: str, senha: str, ativo: bool):
    usuario = get_user(usuario_id, usage=True)
    if usuario is None: 
        return None
    
    usuario.nome = nome
    usuario.email = email
    usuario.senha = senha
    usuario.ativo = ativo
    print("nome: ", nome)
    print("email: ", email)
    print("senha: ", senha)
    print("ativo: ", ativo)
    print("Usuario: ", usuario)

    
    db.session.commit()
    db.session.refresh(usuario)
    return usuario.to_dict()

def delete_user(usuario_id: int):
    usuario = get_user(usuario_id, usage=True)
    if usuario is None:
        return None
    usuario.ativo = False
    usuario.nome = ''
    usuario.email = ''
    usuario.senha = ''
    
    print("Usuario: ", usuario)
    db.session.commit()
    db.session.refresh(usuario)
    create_historic_exclusion(usuario_id)
    return usuario.to_dict()

def create_term(versao: str, atual: bool):
    novo_termo = Termo(versao=versao, atual=atual)
    
    db.session.add(novo_termo)
    db.session.commit()
    db.session.refresh(novo_termo)
    return novo_termo.to_dict()

def get_term(termo_id: int, usage=False):
    termo = db.session.query(Termo).filter(Termo.id == termo_id).first()
    if usage:
        return termo
    return termo.to_dict()

def get_term_all():
    termos = db.session.query(Termo).all()
    return [termo.to_dict() for termo in termos]

def update_term(termo_id: int, versao: str, atual: bool):
    termo = get_term(termo_id, usage=True)
    if termo is None:
        return None
    termo.versao = versao
    termo.atual = atual
    
    db.session.commit()
    db.session.refresh(termo)
    return termo.to_dict()

def delete_term(termo_id: int):
    termo = get_term(termo_id, usage=True)
    if termo is None:
        return None
    
    db.session.delete(termo)
    db.session.commit()
    return termo    

def create_item_term(id_termo: int, descricao: str, obrigatorio: bool):
    novo_item_termo = ItemTermo(id_termo=id_termo, descricao=descricao, obrigatorio=obrigatorio)
    
    db.session.add(novo_item_termo)
    db.session.commit()
    db.session.refresh(novo_item_termo)
    return novo_item_termo

def get_item_term(item_termo_id: int, usage=False):
    item_termo = db.session.query(ItemTermo).filter(ItemTermo.id == item_termo_id).first()
    if usage:
        return item_termo
    return item_termo.to_dict()

def get_item_term_all():
    items_termos = db.session.query(ItemTermo).all()
    return [item_termo.to_dict() for item_termo in items_termos]

def update_item_term(item_termo_id: int, id_termo: int, descricao: str, obrigatorio: bool):
    item_termo = get_item_term(item_termo_id, usage=True)
    if item_termo is None:
        return None
    item_termo.id_termo = id_termo
    item_termo.descricao = descricao
    item_termo.obrigatorio = obrigatorio
    
    db.session.commit()
    db.session.refresh(item_termo)
    return item_termo

def delete_item_term(item_termo_id: int):
    item_termo = get_item_term(item_termo_id, usage=True)
    if item_termo is None:
        return None
    
    db.session.delete(item_termo)
    db.session.commit()
    return item_termo

def create_consent(id_usuario: int, id_item_termo: int, aceite_recusa: bool):
    novo_consentimento = Consentimento(id_usuario=id_usuario, id_item_termo=id_item_termo, aceite_recusa=aceite_recusa)
    db.session.add(novo_consentimento)
    db.session.commit()
    db.session.refresh(novo_consentimento)
    return novo_consentimento.to_dict()

def get_consent(consentimento_id: int, usage=False):
    consentimento = db.session.query(Consentimento).filter(Consentimento.id == consentimento_id).first()
    if usage:
        return consentimento
    return consentimento.to_dict()

def get_consent_all():
    consentimentos = db.session.query(Consentimento).all()
    return [consentimento.to_dict() for consentimento in consentimentos]

def update_consent(consentimento_id: int, id_usuario: int, id_item_termo: int, aceite_recusa: bool):
    consentimento = get_consent(consentimento_id, usage=True)
    
    if consentimento is None:
        return None
    consentimento.id_usuario = id_usuario
    consentimento.id_item_termo = id_item_termo
    consentimento.data_aceite = datetime.utcnow()
    consentimento.aceite_recusa = aceite_recusa
    
    db.session.commit()
    db.session.refresh(consentimento)
    return consentimento.to_dict()

def delete_consent(consentimento_id: int):
    consentimento = get_consent(consentimento_id, usage=True)
    
    if consentimento is None:
        return None
    
    db.session.delete(consentimento)
    db.session.commit()
    return consentimento.to_dict()

def create_historic_exclusion(usuario_id: int):
    nova_exclusao = HistoricoExclusao(usuario_id=usuario_id)
    db.session.add(nova_exclusao)
    db.session.commit()
    db.session.refresh(nova_exclusao)
    return nova_exclusao

def get_historic_exclusion(exclusao_id: int, usage=False):
    historico_exclusao = db.session.query(HistoricoExclusao).filter(HistoricoExclusao.id == exclusao_id).first()
    if usage:
        return historico_exclusao
    return historico_exclusao.to_dict() 

def get_historic_exclusion_all(usage=False):
    hitorico_exclusoes = db.session.query(HistoricoExclusao).all()
    if usage:
        return hitorico_exclusoes
    return [historico_exclusao.to_dict() for historico_exclusao in hitorico_exclusoes]

def delete_user_with_historic(usuario_id: int):
    usuario = get_user(usuario_id, usage=True)
    if usuario is None:
        return None
    usuario.ativo = False
    usuario.nome = ''
    usuario.email = ''
    usuario.senha = ''
    db.session.commit()
    db.session.refresh(usuario)
    return usuario.to_dict()

def verify_user_historic_exclusion(usuario_id: int):
    usuario = get_historic_exclusion(usuario_id, usage=True)
    if usuario is None:
        return None
    else:
        delete_user_with_historic(usuario_id)

