from PySide6.QtCore import QThread, Signal

from flashy.digitizers.caen_dt5781.acquisition import CaenDT5781Acquisition
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.models.acquisition_config import AcquisitionConfig

class CaenDT5781AcquisitionWorker(QThread):
    """
    Wrapper class for the acquisition service to be used in a seperate thread.\n
    Specific to Caen's DT5781 digitizer.
    
    :inherits: `PySide6.QtCore.QThread`
    """
    event_dump = Signal(list)
    """:meta private:"""
    
    def __init__(
        self, 
        acquisition: CaenDT5781Acquisition, 
        config: "AcquisitionConfig"
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
        
        # Run acquisition
        try:
            self.acquisition.run(
                self.config,
                self.event_dump
            )
        finally:
            pass
    
    def stop(self):
        """
        Stop the acquisition as requested by the main thread.
        """
        self.acquisition.stop()