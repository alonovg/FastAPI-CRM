from time import sleep

from pydantic import EmailStr
import smtplib

from app.config import settings
from app.tasks.celery_task import celery
from app.tasks.email_template import create_user_confirmation_template


@celery.task
def debug_task():
    sleep(10)
    print("Celery is running!")


@celery.task
def send_user_confirmation_email(user_data: dict, email_to: EmailStr = None):
    email_to_mock = settings.SMTP_USER
    msg_content = create_user_confirmation_template(user_data, email_to_mock)

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg_content)
