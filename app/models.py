from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    senha = Column(String(120), nullable=False)

class Termo(Base):
    __tablename__ = 'termos'

    id = Column(Integer, primary_key=True)
    versao = Column(String(10), nullable=False)
    itens_obrigatorios = Column(String, nullable=False)
    itens_opcionais = Column(String, nullable=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)

class Consentimento(Base):
    __tablename__ = 'consentimentos'  
    id = Column(Integer, primary_key=True)
    
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    
    id_termo = Column(Integer, ForeignKey('termos.id'), nullable=False)
    
    data_aceite = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="consentimentos")
    termo = relationship("Termo", back_populates="consentimentos")

Usuario.consentimentos = relationship("Consentimento", back_populates="usuario")
Termo.consentimentos = relationship("Consentimento", back_populates="termo")

class HistoricoExclusaoDB2(Base):
    __tablename__ = 'historico_exclusao'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)
    data_remocao = Column(DateTime, default=datetime.utcnow)