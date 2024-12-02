from sqlalchemy.orm import Session
from app.models import Usuario, Termo, Consentimento, HistoricoExclusaoDB2

def create_user(db: Session, nome: str, email: str, senha: str):
    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def get_user(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_user_all(db: Session):
    return db.query(Usuario).all()

def update_user(db: Session, usuario_id: int, nome: str, email: str, senha: str):
    usuario = get_user(db, usuario_id)
    if usuario is None:
        return None
    usuario.nome = nome
    usuario.email = email
    usuario.senha = senha
    db.commit()
    db.refresh(usuario)
    return usuario

def delete_user(db: Session, usuario_id: int):
    usuario = get_user(db, usuario_id)
    if usuario is None:
        return None
    db.delete(usuario)
    db.commit()
    return usuario



