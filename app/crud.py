from app.models import Usuario, Termo, Consentimento, HistoricoExclusao, ItemTermo
from .database import db

def create_user(nome: str, email: str, senha: str):
    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def get_user(usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_user_all():
    return db.query(Usuario).all()

def update_user(usuario_id: int, nome: str, email: str, senha: str, ativo: bool):
    usuario = get_user(usuario_id)
    if usuario is None:
        return None
    usuario.nome = nome
    usuario.email = email
    usuario.senha = senha
    usuario.ativo = ativo
    
    db.commit()
    db.refresh(usuario)
    return usuario

def delete_user(usuario_id: int):
    usuario = get_user(usuario_id)
    if usuario is None:
        return None
    
    db.delete(usuario)
    db.commit()
    return usuario

def create_term(versao: str, atual: bool):
    novo_termo = Termo(versao=versao, atual=atual)
    
    db.add(novo_termo)
    db.commit()
    db.refresh(novo_termo)
    return novo_termo

def get_term(termo_id: int):
    
    return db.query(Termo).filter(Termo.id == termo_id).first()

def get_term_all():
    
    return db.query(Termo).all()

def update_term(termo_id: int, versao: str, atual: bool):
    termo = get_term(termo_id)
    if termo is None:
        return None
    termo.versao = versao
    termo.atual = atual
    
    db.commit()
    db.refresh(termo)
    return termo

def delete_term(termo_id: int):
    termo = get_term(termo_id)
    if termo is None:
        return None
    
    db.delete(termo)
    db.commit()
    return termo    

def create_item_term(id_termo: int, descricao: str, obrigatorio: bool):
    novo_item_termo = ItemTermo(id_termo=id_termo, descricao=descricao, obrigatorio=obrigatorio)
    
    db.add(novo_item_termo)
    db.commit()
    db.refresh(novo_item_termo)
    return novo_item_termo

def get_item_term(item_termo_id: int):
    
    return db.query(ItemTermo).filter(ItemTermo.id == item_termo_id).first()

def get_item_term_all():
    
    return db.query(ItemTermo).all()

def update_item_term(item_termo_id: int, id_termo: int, descricao: str, obrigatorio: bool):
    item_termo = get_item_term(item_termo_id)
    if item_termo is None:
        return None
    item_termo.id_termo = id_termo
    item_termo.descricao = descricao
    item_termo.obrigatorio = obrigatorio
    
    db.commit()
    db.refresh(item_termo)
    return item_termo

def delete_item_term(item_termo_id: int):
    item_termo = get_item_term(item_termo_id)
    if item_termo is None:
        return None
    
    db.delete(item_termo)
    db.commit()
    return item_termo

def create_consent(id_usuario: int, id_item_termo: int, id_termo: int):
    novo_consentimento = Consentimento(id_usuario=id_usuario, id_item_termo=id_item_termo, id_termo=id_termo)
    
    db.add(novo_consentimento)
    db.commit()
    db.refresh(novo_consentimento)
    return novo_consentimento

def get_consent(consentimento_id: int):
    
    return db.query(Consentimento).filter(Consentimento.id == consentimento_id).first()

def get_consent_all():
    
    return db.query(Consentimento).all()

def update_consent(consentimento_id: int, id_usuario: int, id_item_termo: int, id_termo: int):
    consentimento = get_consent(consentimento_id)
    
    if consentimento is None:
        return None
    consentimento.id_usuario = id_usuario
    consentimento.id_item_termo = id_item_termo
    consentimento.id_termo = id_termo
    
    db.commit()
    db.refresh(consentimento)
    return consentimento

def delete_consent(consentimento_id: int):
    consentimento = get_consent(consentimento_id)
    
    if consentimento is None:
        return None
    
    db.delete(consentimento)
    db.commit()
    return consentimento

def create_historic_exclusion(usuario_id: int):
    nova_exclusao = HistoricoExclusao(usuario_id=usuario_id)
    db.add(nova_exclusao)
    db.commit()
    db.refresh(nova_exclusao)
    return nova_exclusao

def get_historic_exclusion(exclusao_id: int):
    
    return db.query(HistoricoExclusao).filter(HistoricoExclusao.id == exclusao_id).first()

def get_historic_exclusion_all():
    
    return db.query(HistoricoExclusao).all()


