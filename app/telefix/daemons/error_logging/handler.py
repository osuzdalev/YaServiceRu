from functools import partial
import smtplib as smtp

from .error_logging import error_notification
from ...common.types import TgModuleType


class ErrorHandler:
    name = TgModuleType.ERROR_LOGGING

    def __init__(self, smtp_url, smtp_port):
        self.server = self.init_mail_server(smtp_url, smtp_port)

        self.error_notification = partial(error_notification, mail_server=self.server)

    def init_mail_server(self, smtp_url, smtp_port):
        server = smtp.SMTP(smtp_url, smtp_port)
        # TODO use the  loguru log level as argument here
        server.set_debuglevel(0)
        server.starttls()

        return server

    def get_handler(self):
        return self.error_notification
