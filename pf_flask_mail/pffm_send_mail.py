import smtplib
import ssl
import threading
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import exists
from pathlib import Path
from pf_flask_mail.common.pffm_config import PFFMConfig


class PFFMSendMail(threading.Thread):
    close_connection: bool = True
    smtp_server: smtplib.SMTP_SSL = None
    config: PFFMConfig = None
    _email_content: MIMEMultipart = MIMEMultipart('alternative')
    _email_to: list = []

    def __init__(self, config: PFFMConfig):
        self.config = config
        threading.Thread.__init__(self)

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
            raise e

    def compose(self, to, subject):
        self._email_content = MIMEMultipart('alternative')
        self._email_to = []
        if isinstance(to, list):
            self._email_content['To'] = ",".join(to)
            self._email_to = to
        else:
            self._email_content['To'] = to
            self._email_to.append(to)
        self._email_content['Subject'] = subject
        return self

    def add_text_message(self, message: str):
        self._email_content.attach(MIMEText(message, 'plain'))

    def add_html_message(self, html: str, text: str = None):
        self._email_content.attach(MIMEText(html, 'html'))
        if text:
            self._email_content.attach(MIMEText(text, 'plain'))

    def add_attachment(self, file_path):
        try:
            if exists(file_path):
                with open(file_path, "rb") as attachment:
                    attachment_mime = MIMEBase("application", "octet-stream")
                    attachment_mime.set_payload(attachment.read())
                encoders.encode_base64(attachment_mime)
                filename = Path(file_path).name
                attachment_mime.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                )
                self._email_content.attach(attachment_mime)
                self._email_content.replace_header("Content-Type", "multipart/mixed")
        except Exception as e:
            raise e

    def add_cc(self, cc):
        cc_text = ""
        if isinstance(cc, list):
            self._email_to += cc
            cc_text += ",".join(cc)
        else:
            self._email_to.append(cc)
            cc_text += cc
        self._email_content['CC'] = cc_text

    def add_bcc(self, bcc):
        if isinstance(bcc, list):
            self._email_to += bcc
        else:
            self._email_to.append(bcc)

    def run(self):
        try:
            self._init_server()
            sender = self.config.smtpSenderEmail
            if not sender:
                sender = self.config.smtpUser
            self.smtp_server.sendmail(sender, self._email_to, self._email_content.as_string())
        except Exception as e:
            raise e
        finally:
            if self.close_connection:
                self.smtp_server.close()

    def send(self, close_connection: bool = True, use_thread: bool = False):
        self.close_connection = close_connection
        if use_thread:
            self.start()
        else:
            self.run()
