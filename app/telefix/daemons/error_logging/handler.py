from functools import partial
import smtplib as smtp

from .error_logging import error_notification
from ...common.types import TgModuleType


class ErrorHandler:
    TYPE = TgModuleType.ERROR_LOGGING

    def __init__(self, smtp_url, smtp_port, log_level: str):
        self.server = self._init_mail_server(smtp_url, smtp_port, log_level)

        self.error_notification = partial(error_notification, mail_server=self.server)

    @staticmethod
    def _init_mail_server(smtp_url: str, smtp_port: int, log_level: str):
        server = smtp.SMTP(smtp_url, smtp_port)
        # INFO == 0, DEBUG == 1+
        if log_level == "INFO":
            server.set_debuglevel(0)
        else:
            server.set_debuglevel(1)
        server.starttls()

        return server

    def get_handler(self):
        return self.error_notification
