import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from database import Usuario

def enviar_notificacao(email_destino, assunto, mensagem):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    EMAIL = 'nocloud76@gmail.com'
    EMAIL_PASSWORD = 'fngq edxc vwsz wukl'

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = email_destino
    msg['Subject'] = assunto

    msg.attach(MIMEText(mensagem, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        texto = msg.as_string()
        server.sendmail(EMAIL, email_destino, texto)
        server.quit()
        print("Notificação enviada com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar notificação: {e}")

def verificar_e_enviar_notificacao(user_id, assunto, mensagem):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    usuario = session.query(Usuario).filter_by(id=user_id).first()
    if usuario and usuario.ativo:
        enviar_notificacao(usuario.email, assunto, mensagem)
    else:
        print("Usuário não encontrado ou inativo.")

# Exemplo de uso
verificar_e_enviar_notificacao(1, "Notificação de Intercorrência nos Dados Pessoais", "Houve uma alteração nos seus dados pessoais.")