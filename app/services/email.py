import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_verification_email(email: str, token: str):

    backend_url = os.getenv(
        "BACKEND_URL",
        "http://127.0.0.1:8000"
    )

    verification_url = (
        f"{backend_url}/auth/verify-email"
        f"?token={token}"
    )

    message = EmailMessage()

    message["Subject"] = "Verify your SIH account"
    message["From"] = os.getenv("SMTP_USERNAME")
    message["To"] = email

    message.set_content(
        f"""
Hello,

Please verify your SIH account using this link:

{verification_url}

This link expires in 30 minutes.
"""
    )

    with smtplib.SMTP(
        os.getenv("SMTP_HOST"),
        int(os.getenv("SMTP_PORT", "587"))
    ) as server:

        server.starttls()

        server.login(
            os.getenv("SMTP_USERNAME"),
            os.getenv("SMTP_PASSWORD")
        )

        server.send_message(message)


def send_reset_email(email: str, token: str):

    backend_url = os.getenv(
        "BACKEND_URL",
        "http://127.0.0.1:8000"
    )

    reset_url = (
        f"{backend_url}/auth/reset-password"
        f"?token={token}"
    )

    message = EmailMessage()

    message["Subject"] = "Reset your SIH password"
    message["From"] = os.getenv("SMTP_USERNAME")
    message["To"] = email

    message.set_content(
        f"""
Hello,

We received a request to reset your SIH password.

Use this link:

{reset_url}

This link expires in 30 minutes.

If you did not request this, ignore this email.
"""
    )

    with smtplib.SMTP(
        os.getenv("SMTP_HOST"),
        int(os.getenv("SMTP_PORT", "587"))
    ) as server:

        server.starttls()

        server.login(
            os.getenv("SMTP_USERNAME"),
            os.getenv("SMTP_PASSWORD")
        )

        server.send_message(message)