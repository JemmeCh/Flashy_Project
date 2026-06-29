from enum import Enum, auto

class AcquisitionState(Enum):
    """
    Enumeration of acquisition system states.
    
    This enum represents the lifecycle states of the acquisition system,
    from initial disconnection to active acquisition and error handling.
    
    Attributes:
        DISCONNECTED: No connection to the acquisition hardware.
        CONNECTING: Attempting to establish a connection.
        READY: System is connected and ready to start acquisition.
        ACQUIRING: Data acquisition is currently in progress.
        STOPPING: Acquisition is in the process of stopping.
        ERROR: An error state indicating acquisition failure or invalid state.
    """
    DISCONNECTED = auto()
    CONNECTING = auto()
    READY = auto()
    ACQUIRING = auto()
    STOPPING = auto()
    ERROR = auto()