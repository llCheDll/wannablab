import logging
import logging.handlers as handlers
import sys

from config import settings


class Logger:
    def __init__(self, name='logger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(settings.logging.level)

        if settings.debug:
            self.handler = logging.StreamHandler(stream=sys.stdout)
        else:
            self.handler = handlers.RotatingFileHandler(
                filename=settings.logging.filename,
                mode='a',
                maxBytes=settings.logging.maxBytes,
                backupCount=settings.logging.backupCount,
            )
        self.formatter = logging.Formatter(
            settings.logging.format,
        )
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
