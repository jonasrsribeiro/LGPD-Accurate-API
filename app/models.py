from datetime import datetime
from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

class Consentimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_termo = db.Column(db.Integer, db.ForeignKey('termo.id'), nullable=False)
    data_aceite = db.Column(db.DateTime, default=datetime.utcnow)

class Termo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    versao = db.Column(db.String(10), nullable=False)
    itens_obrigatorios = db.Column(db.Text, nullable=False)
    itens_opcionais = db.Column(db.Text, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)