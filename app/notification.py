import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config  # Importação absoluta
from app.models import Usuario  # Importação absoluta

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
        print(f"Notificação enviada para {email_destino}")
    except Exception as e:
        print(f"Falha ao enviar notificação: {e}")

def enviar_notificacoes_para_todos(assunto, mensagem):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    usuarios = session.query(Usuario).filter_by(ativo=True).all()
    for usuario in usuarios:
        enviar_notificacao(usuario.email, assunto, mensagem)
        print(f"Notificação enviada para {usuario.email}")

if __name__ == "__main__":
    assunto = "Notificação de Segurança"
    mensagem = "Houve um problema de segurança e seus dados podem ter sido comprometidos. Por favor, tome as medidas necessárias."
    enviar_notificacoes_para_todos(assunto, mensagem)