import msgspec

class BaseDetector(msgspec.Struct):
    def get_vmus_to_nc_factor(self) -> float:
        ...