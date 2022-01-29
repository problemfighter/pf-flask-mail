import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pf_flask_mail.common.pffm_config import PFFMConfig


class PFFMSendMail:
    smtp_server: smtplib.SMTP_SSL = None
    config: PFFMConfig = None
    _email_content: MIMEMultipart = MIMEMultipart('alternative')
    _email_to: str = None

    def __init__(self, config: PFFMConfig):
        self.config = config

    def _init_server(self):
        try:
            ssl_context = ssl.create_default_context()
            if self.config.smtpEncryption == "tls":
                self.smtp_server = smtplib.SMTP_SSL(self.config.smtpServer, self.config.smtpPort)
                self.smtp_server.starttls(context=ssl_context)
            else:
                self.smtp_server = smtplib.SMTP_SSL(self.config.smtpServer, self.config.smtpPort, context=ssl_context)
            self.smtp_server.login(self.config.smtpUser, self.config.smtpPassword)
        except Exception as e:
            print(e)

    def compose(self, to, subject):
        self._email_content['To'] = self._email_to = to
        self._email_content['Subject'] = subject
        return self

    def add_text_message(self, message: str):
        self._email_content.attach(MIMEText(message, 'plain'))

    def add_html_message(self, html: str, text: str = None):
        pass

    def add_attachment(self):
        pass

    def add_cc(self):
        pass

    def add_bcc(self):
        pass

    def add_individual_recipient(self, single: str = None, multiple: list = None):
        pass

    def send(self):
        try:
            sender = self.config.smtpSenderEmail
            if not sender:
                sender = self.config.smtpUser
            self.smtp_server.sendmail(sender, self._email_to, self._email_content.as_string())
        except Exception as e:
            print(e)
