from PySide6 import QtCore as qtc

class LogEmitter(qtc.QObject):
    """
    Qt-based signal emitter for logging messages.
    
    This QObject provides a thread-safe signal that can be used to transmit
    log messages from non-GUI threads to Qt GUI components.
    
    Signals:
        message_logged (str, int): 
            Emitted when a log message is produced.
            The first argument is the formatted log message, and the second
            argument is the logging level (e.g., logging.INFO, logging.ERROR).
    """
    message_logged = qtc.Signal(str, int)

emitter = LogEmitter()
"""
Global instance of :class:`LogEmitter`.

This singleton emitter is used by logging handlers to broadcast log
messages throughout the application, typically to GUI components.
"""