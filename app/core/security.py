from datetime import datetime, timedelta, timezone
import os
from jose import jwt
from app.core.config import settings
import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

def create_access_token(subject: str, minutes: int, token_type: str, role: str):
    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=minutes)).timestamp()),
        "type": token_type,
        "role": role,
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

def create_verification_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "type": "email_verification",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=24)).timestamp()),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Email information function (simulated)


def send_email(to_email: str, subject: str, body: str):
    print(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_SENDER
    msg['To'] = to_email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
        smtp_server.sendmail(settings.EMAIL_SENDER, to_email, msg.as_string())

def send_verification_email(user_email: str, user_id: int):
    token = create_verification_token(user_id)
    verification_link = f"{settings.EMAIL_SERVER_HOST}/users/{user_id}/verify?token={token}"

    send_email(
        to_email=user_email,
        subject=settings.EMAIL_SUBJECT,
        body=f"Please verify your email by clicking on the following link: {verification_link}"
    )

    # print(f"Send verification email to {user_email} with link: {verification_link}")
