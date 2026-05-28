from PySide6.QtCore import QThread, Signal

from src.digitizers.caen_dt5781.acquisition import CaenDT5781Acquisition
from src.models.data_config import AcquisitionConfig

class CaenCT5781AcquisitionWorker(QThread):
    event_dump = Signal(list)
    error = Signal(str)# NOTE: Check if usefull
    
    def __init__(self, acquisition: CaenDT5781Acquisition, config: AcquisitionConfig) -> None:
        super().__init__()
        self.acquisition = acquisition
        self.config = config
    
    def run(self):
        """Run an acquisition"""
        # Check if there's a config
        if not self.config:
            raise ValueError("Please add a config at instantiation")
        
        # Connect callback to signals
        self.acquisition.event_dump_callback = self.event_dump.emit # type:ignore
        self.acquisition.error_callback = self.error.emit # type:ignore
        
        # Run acquisition
        try:
            self.acquisition.run(self.config)
        finally:
            pass
    
    def stop(self):
        """Request stop from main thread"""
        self.acquisition.stop()