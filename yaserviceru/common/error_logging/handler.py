from yaserviceru.common.error_logging.error_logging import error_notification


class ErrorHandler:
    def __init__(self):
        self.error_notification = error_notification

    def get_handler(self):
        return self.error_notification
