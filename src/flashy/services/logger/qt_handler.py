import logging

from src.flashy.services.logger.emitter import emitter

class QtHandler(logging.Handler):
    def __init__(self):
        super().__init__()
    
    def emit(self, record):
        record = logging.LogRecord(
            record.name,
            record.levelno,
            record.pathname,
            record.lineno,
            record.msg,
            record.args,
            exc_info=None
        )
        
        msg = self.format(record)
        emitter.message_logged.emit(msg, record.levelno)