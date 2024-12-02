from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    nome = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

class Termo(db.Model):
    __tablename__ = 'termos'

    id = db.Column(db.Integer, primary_key=True)
    versao = db.Column(db.String(10), nullable=False)
    atual = db.Column(db.Boolean, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship("ItemTermo", back_populates="termo")

class ItemTermo(db.Model):
    __tablename__ = 'itens_termos'

    id = db.Column(db.Integer, primary_key=True)
    id_termo = db.Column(db.Integer, db.ForeignKey('termos.id'), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    obrigatorio = db.Column(db.Boolean, nullable=False)
    termo = db.relationship("Termo", back_populates="itens")
    consentimentos = db.relationship("Consentimento", back_populates="item_termo")

class Consentimento(db.Model):
    __tablename__ = 'consentimentos'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    id_item_termo = db.Column(db.Integer, db.ForeignKey('itens_termos.id'), nullable=False)
    id_termo = db.Column(db.Integer, db.ForeignKey('termos.id'), nullable=False)
    data_aceite = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.relationship("Usuario", back_populates="consentimentos")
    item_termo = db.relationship("ItemTermo", back_populates="consentimentos")

class HistoricoExclusao(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'historico_exclusoes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    data_remocao = db.Column(db.DateTime, default=datetime.utcnow)

# Adicione os relacionamentos ausentes
Usuario.consentimentos = db.relationship("Consentimento", back_populates="usuario")
