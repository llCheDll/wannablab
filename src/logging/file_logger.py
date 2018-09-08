import logging
import logging.handlers

from config import settings

class FileLogger():
    def __init__(self, name='logger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(settings.logging.fileLogger.level)
        self.handler = logging.handlers.RotatingFileHandler(
            filename=settings.logging.fileLogger.filename,
            mode='a',
            maxBytes=settings.logging.fileLogger.maxBytes,
            backupCount=settings.logging.fileLogger.backupCount,
        )
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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
