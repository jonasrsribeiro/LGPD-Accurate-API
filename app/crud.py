from sqlalchemy.orm import Session
from app.models import User, Term, Consent, HistoricoExclusaoDB2

def create_user(db: Session, name: str, email: str, password: str):
    new_user = User(name=name, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


