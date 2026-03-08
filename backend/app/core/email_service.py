import smtplib
from email.mime.text import MIMEText

from app.core.config import settings


class SMTPEmailService:
    def send_email(self, to_email: str, subject: str, body: str) -> None:
        if not settings.smtp_username or not settings.smtp_password or not settings.smtp_sender:
            return
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = settings.smtp_sender
        message["To"] = to_email

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.smtp_sender, [to_email], message.as_string())
