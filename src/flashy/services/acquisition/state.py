from enum import Enum, auto

class AcquisitionState(Enum):
    DISCONNECTED = auto()
    CONNECTING = auto()
    READY = auto()
    ACQUIRING = auto()
    STOPPING = auto()
    ERROR = auto()