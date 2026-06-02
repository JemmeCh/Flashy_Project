from PySide6.QtCore import QThread, Signal

from flashy.digitizers.caen_dt5781.acquisition import CaenDT5781Acquisition
from flashy.models.processing_config import AcquisitionConfig

class CaenDT5781AcquisitionWorker(QThread):
    """
    Wrapper class for the acquisition service to be used in a seperate thread.\n
    Specific to Caen's DT5781 digitizer.
    
    :inherits: `PySide6.QtCore.QThread`
    """
    event_dump = Signal(list)
    """:meta private:"""
    error = Signal(str)# NOTE: Check if usefull
    """:meta private:"""
    
    def __init__(
        self, 
        acquisition: CaenDT5781Acquisition, 
        config: AcquisitionConfig
    ) -> None:
        super().__init__()
        self.acquisition = acquisition
        self.config = config
    
    def run(self):
        """
        Start the acquisition of new data.
        """
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
        """
        Stop the acquisition as requested by the main thread.
        """
        self.acquisition.stop()