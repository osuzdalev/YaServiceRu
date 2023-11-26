from functools import partial
import smtplib as smtp

from .error_logging import error_notification


class ErrorHandler:
    def __init__(self, smtp_url, smtp_port):
        self.server = self.init_mail_server(smtp_url, smtp_port)

        self.error_notification = partial(error_notification, mail_server=self.server)

    def init_mail_server(self, smtp_url, smtp_port):
        server = smtp.SMTP(smtp_url, smtp_port)
        server.set_debuglevel(1)
        server.starttls()

        return server

    def get_handler(self):
        return self.error_notification
