from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = 'users'  
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)  # Encriptado

class Term(Base):
    __tablename__ = 'terms'

    id = Column(Integer, primary_key=True)
    version = Column(String(10), nullable=False)
    mandatory_items = Column(String, nullable=False)
    optional_items = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Consent(Base):
    __tablename__ = 'consents'  
    id = Column(Integer, primary_key=True)
    
    # Chave estrangeira para a tabela 'users'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Chave estrangeira para a tabela 'terms'
    term_id = Column(Integer, ForeignKey('terms.id'), nullable=False)
    
    accepted_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="consents")
    term = relationship("Term", back_populates="consents")

User.consents = relationship("Consent", back_populates="user")
Term.consents = relationship("Consent", back_populates="term")

class HistoricoExclusaoDB2(Base):
    __tablename__ = 'historico_exclusao'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    deleted_at = Column(DateTime, default=datetime.utcnow)