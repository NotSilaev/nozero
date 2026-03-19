from src.core.config import settings

from src.exceptions.mails import EmailSendingError

from smtplib import SMTP_SSL
from email.mime.text import MIMEText


class MailsService:
    @staticmethod
    def send_mail(recipients: tuple, subject: str, content: str, content_subtype: str = "plain") -> None:
        if len(recipients) < 1:
            raise EmailSendingError("An email must have at least one recipient")

        sender = settings.SMTP_FROM

        try:
            message = MIMEText(content, content_subtype)
            message["Subject"] = subject
            message["From"] = sender

            connection = SMTP_SSL(settings.SMTP_HOST)
            connection.set_debuglevel(False)
            connection.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

            try:
                connection.sendmail(sender, recipients, message.as_string())
            finally:
                connection.quit()

        except Exception as e:
            raise EmailSendingError(e)
