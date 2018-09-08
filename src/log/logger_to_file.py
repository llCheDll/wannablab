import logging
import logging.handlers

from config import settings


class LoggerToFile():
    def __init__(self, name='logger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(settings.logging.LoggerToFile.level)
        self.handler = logging.handlers.RotatingFileHandler(
            filename=settings.logging.LoggerToFile.filename,
            mode='a',
            maxBytes=settings.logging.LoggerToFile.maxBytes,
            backupCount=settings.logging.LoggerToFile.backupCount,
        )
        self.formatter = logging.Formatter(
            settings.logging.LoggerToFile.format,
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
