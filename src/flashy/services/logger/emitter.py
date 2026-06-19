from PySide6 import QtCore as qtc

class LogEmitter(qtc.QObject):
    message_logged = qtc.Signal(str, int)

emitter = LogEmitter()