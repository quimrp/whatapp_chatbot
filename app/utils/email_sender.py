import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

def send_email(to_email: str, subject: str, body: str):
    # Configuración del servidor SMTP (ejemplo con Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = settings.EMAIL_USERNAME
    smtp_password = settings.EMAIL_PASSWORD

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = to_email
    message["Subject"] = subject

    # Añadir el cuerpo del mensaje
    message.attach(MIMEText(body, "plain"))

    # Iniciar sesión en el servidor SMTP y enviar el correo
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        print(f"Correo enviado exitosamente a {to_email}")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")

