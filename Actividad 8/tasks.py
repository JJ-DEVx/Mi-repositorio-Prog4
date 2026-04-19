from celery_app import celery
from flask_mail import Mail, Message
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

@celery.task
def enviar_correo(asunto, destinatario, mensaje):
    try:
        with app.app_context():
            msg = Message(
                asunto,
                sender=app.config['MAIL_USERNAME'],
                recipients=[destinatario]
            )
            msg.body = mensaje
            mail.send(msg)
    except Exception as e:
        print("Error enviando correo:", e)