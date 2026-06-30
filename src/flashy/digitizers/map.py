from flashy.digitizers.info import DigitizerInfo
from flashy.digitizers.dummy.config import DummyDigitizerConfig
from flashy.digitizers.caen_dt5781.config import CaenDT5781Config

DIGITIZER_MAP = {
    "caen_dt5781": DigitizerInfo(
        key="caen_dt5781",
        display_name="Caen DT5781A",
        config_cls=CaenDT5781Config,
        tag_cls="caendt5781config"
    ),
    "dummy": DigitizerInfo(
        key="dummy",
        display_name="Dummy Digitizer",
        config_cls=DummyDigitizerConfig,
        tag_cls="dummydigitizerconfig",
    ),
}