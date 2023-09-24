from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_user_confirmation_template(user_data: dict, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Confirm your email address"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Hi {user_data["name"]}</h1>
            Please confirm your email address by clicking on the following link:
            {settings.FRONTEND_URL}/confirm-email/{user_data["id"]}
            If you did not request this, please ignore this email.
        """)
    return email
