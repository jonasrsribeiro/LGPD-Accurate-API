from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    senha = Column(String(120), nullable=False)
    ativo = Column(Boolean, default=True)

    consentimentos = relationship("Consentimento", back_populates="usuario")

class Termo(Base):
    __tablename__ = 'termos'

    id = Column(Integer, primary_key=True)
    versao = Column(String(10), nullable=False)
    atual = Column(Boolean, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    itens = relationship("ItemTermo", back_populates="termo")

class ItemTermo(Base):
    __tablename__ = 'itens_termos'

    id = Column(Integer, primary_key=True)
    id_termo = Column(Integer, ForeignKey('termos.id'), nullable=False)
    descricao = Column(String, nullable=False)
    obrigatorio = Column(Boolean, nullable=False)
    termo = relationship("Termo", back_populates="itens")
    consentimentos = relationship("Consentimento", back_populates="item_termo")

class Consentimento(Base):
    __tablename__ = 'consentimentos'

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_item_termo = Column(Integer, ForeignKey('itens_termos.id'), nullable=False)
    
    id_termo = Column(Integer, ForeignKey('termos.id'), nullable=False)
    data_aceite = Column(DateTime, default=datetime.utcnow)
    usuario = relationship("Usuario", back_populates="consentimentos")
    item_termo = relationship("ItemTermo", back_populates="consentimentos")

class HistoricExclusion(Base):
    __tablename__ = 'historico_exclusoes'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)
    data_remocao = Column(DateTime, default=datetime.utcnow)
