import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_notificacao(email_destino, assunto, mensagem):
    email_origem = 'seu_email@example.com'
    senha = 'sua_senha'

    msg = MIMEMultipart()
    msg['From'] = email_origem
    msg['To'] = email_destino
    msg['Subject'] = assunto

    msg.attach(MIMEText(mensagem, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(email_origem, senha)
        texto = msg.as_string()
        server.sendmail(email_origem, email_destino, texto)
        server.quit()
        print("Notificação enviada com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar notificação: {e}")

def verificar_intercorrencia(dados_atuais, novos_dados):
    if dados_atuais != novos_dados:
        assunto = "Notificação de Intercorrência nos Dados Pessoais"
        mensagem = "Houve uma alteração nos seus dados pessoais."
        enviar_notificacao('destinatario@example.com', assunto, mensagem)

# Exemplo de uso
dados_atuais = {'nome': 'João', 'email': 'joao@example.com'}
novos_dados = {'nome': 'João', 'email': 'joao_novo@example.com'}

verificar_intercorrencia(dados_atuais, novos_dados)