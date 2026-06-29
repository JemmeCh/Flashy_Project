import logging

from flashy.services.logger.emitter import emitter

class QtHandler(logging.Handler):
    """
    Logging handler that forwards log records to the Qt event system.
    
    This handler formats log records and emits them through a Qt signal,
    allowing log messages to be displayed safely in the graphical user
    interface.
    """
    def __init__(self):
        super().__init__()
    
    def emit(self, record):
        """
        Emit a log record through the Qt logging signal.
        
        .. important::
            A new :class:`logging.LogRecord` is created **without exception
            information** to not clutter the GUI log terminal.
        
        :param record: Log record to emit.
        :type record: logging.LogRecord
        
        :returns: None
        :rtype: None
        """
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