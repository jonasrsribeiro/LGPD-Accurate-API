from sqlalchemy.orm import Session
from app.models import User, Term, Consent, HistoricoExclusaoDB2

def create_user(db: Session, name: str, email: str, password: str):
    new_user = User(name=name, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_all(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, name: str, email: str, password: str):
    user = get_user(db, user_id)
    if user is None:
        return None
    user.name = name
    user.email = email
    user.password = password
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user is None:
        return None
    db.delete(user)
    db.commit()
    return user



