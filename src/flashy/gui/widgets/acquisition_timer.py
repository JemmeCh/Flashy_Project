from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

class AcquisitionTimer(qtw.QLCDNumber):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSegmentStyle(qtw.QLCDNumber.SegmentStyle.Filled)
        self.setDigitCount(9)
        
        self._timer = qtc.QTimer(self)
        self._timer.timeout.connect(self._show_time)
        
        self._elapsed_timer = qtc.QElapsedTimer()
        self.display('00:00:000')
    
    def toggle_timer(self):
        if self._timer.isActive(): 
            self._stop_timer()
        else: 
            self._start_timer()
    
    def _start_timer(self):
        self._elapsed_timer.start()
        self._timer.start(10)
        
    def _stop_timer(self):
        self._timer.stop()
        self.display('00:00:000')
    
    @qtc.Slot()
    def _show_time(self):
        elapsed_ms = self._elapsed_timer.elapsed()
        
        minutes = elapsed_ms // 60000
        seconds = (elapsed_ms % 60000) // 1000
        milliseconds = elapsed_ms % 1000
        text = f"{minutes:02}:{seconds:02}:{milliseconds:03}"
        
        # Blinking effect
        if (seconds % 2) == 0:
            text = text.replace(":", " ")
        
        self.display(text)