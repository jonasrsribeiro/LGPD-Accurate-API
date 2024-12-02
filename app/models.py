from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = 'users'  
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)  # Encriptado

class Terms(Base):
    __tablename__ = 'terms'

    id = Column(Integer, primary_key=True)
    version = Column(String(10), nullable=False)
    current = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ItemTerm(Base):
    __tablename__ = 'items_terms'

    id = Column(Integer, primary_key=True)
    term_id = Column(Integer, ForeignKey('terms.id'), nullable=False)
    item = Column(String, nullable=False)
    required = Column(Boolean, default=False)
    description = Column(String, nullable=False)
    
    term = relationship("Term", back_populates="items")

class Consent(Base):
    __tablename__ = 'consents'  
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_term_id = Column(Integer, ForeignKey('items_terms.id'), nullable=False)
    
    accepted_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="consents")
    term = relationship("Term", back_populates="consents")

User.consents = relationship("Consent", back_populates="user")
Terms.consents = relationship("Consent", back_populates="term")

class HistoricExclusion(Base):
    __tablename__ = 'historic_exclusions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    deleted_at = Column(DateTime, default=datetime.utcnow)