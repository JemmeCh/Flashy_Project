from typing import  Any, List
from functools import wraps

from caen_felib import lib, device, error
print(f'CAEN FELib wrapper loaded (lib version {lib.version})')

from src.models.data_config import AcquisitionConfig
from src.digitizers.caen_dt5781.channel import CaenDT5781Channel


def handle_CAEN_exceptions(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except error.Error as ex:
            if ex.code.value == error.ErrorCode.COMMAND_ERROR:
                print(f"Error code {ex.code.value} (COMMAND_ERROR): Couldn't find a digitizer to connect to!")
            else:
                print(f"Error code {ex.code.value}: Unexpected! Raising error (see terminal)")
                raise
        finally:
            self._cleanup()
    return wrapper

class CaenDT5781Acquisition:
    def __init__(self) -> None:
        self.uri = self._make_uri()
        
        self._stop_requested = False
        self.event_dump_callback = None # Set by worker
        self.error_callback = None # Set by worker
    
    # =======================================================================
    # Digitizer interaction methods
    # =======================================================================
    
    @handle_CAEN_exceptions
    def get_basic_info(self) -> dict[str, Any]:
        self._stop_requested = False
        if not self._can_use_digitizer():
            raise ConnectionError('The digitizer is unavailable')
        
        with device.connect(self.uri) as dig:
            print("Digitizer connected! Retreiving basic info...")
            #self.model_controller.controller.isGETTING_BASIC_INFO = True
            # Change status
            #self.change_aqc_panel_status("Connecté")
            
            # First connection
            #self.model_controller.controller.hasDIGITIZERCONNECTED = True
            
            # Reset
            dig.cmd.RESET()
            
            # Get digitizer information
            name:str = dig.par.MODELNAME.value # str
            familycode:str = dig.par.FAMILYCODE.value # str
            fw_type:str = dig.par.FWTYPE.value # str
            serial_num:int = int(dig.par.SERIALNUM.value) # number
            adc_n_bits:int = int(dig.par.ADC_NBIT.value) # number
            adc_samplrate_msps:float = float(dig.par.ADC_SAMPLRATE.value)  # number in Msps
            sampling_period_ns:int = int(1e3 / adc_samplrate_msps)
            max_rawdata_size:float = float(dig.par.MAXRAWDATASIZE.value) # number
        self._stop_requested = True
        return {
            'model_name': name,
            'family_code': familycode,
            'fw_type': fw_type,
            'serial_num': serial_num,
            'adc_n_bits': adc_n_bits,
            'adc_samplrate_msps': adc_samplrate_msps,
            'sampling_period_ns': sampling_period_ns,
            'max_rawdata_size': max_rawdata_size
        }
    
    @handle_CAEN_exceptions
    def run(self, acquisition_config: AcquisitionConfig):
        self._stop_requested = False
        print('Attempting to connect to digitizer...')
        with device.connect(self.uri) as dig:
            print("Connected! Configurating parameters")
            data, endpoint = self._setup_digitizer(dig, acquisition_config)
            
            # Get reference to data fields
            channel = data[0].value
            flags = data[1].value
            timestamp = data[2].value
            energy = data[3].value
            analog_probe_1 = data[4].value
            analog_probe_1_type = data[5].value  # Integer value described in Supported Endpoints > Probe type meaning
            digital_probe_1 = data[6].value
            digital_probe_1_type = data[7].value  # Integer value described in Supported Endpoints > Probe type meaning
            waveform_size = data[8].value
            
            # Start acquisition
            dig.cmd.ARMACQUISITION()
            k = 0
            # Save file as running
            all_detect = []
            
            print("Digitizer configured! Starting Acquisition...")
            while not self._stop_requested:
                dig.cmd.SENDSWTRIGGER()
                
                try:
                    endpoint.read_data(10, data)
                    # CHANNEL ALWAYS FIRST, SAMPLES ALWAYS LAST
                    all_detect.append([ # We don't use the other values 
                        channel.copy(), flags.copy(), #type:ignore
                        waveform_size.copy(), analog_probe_1.copy()
                    ])
                except error.Error as ex:
                    if ex.code == error.ErrorCode.TIMEOUT:
                        continue
                    elif ex.code == error.ErrorCode.STOP:
                        break
                    else:
                        raise ex
                
                assert analog_probe_1_type == 1  # 1 -> 'VPROBE_INPUT'
                assert digital_probe_1_type == 26  # 26 -> 'VPROBE_TRIGGER'
                
                # Dump data to be analysed
                if k > 10000 and self.event_dump_callback:
                    batch = all_detect
                    all_detect = []
                    self.event_dump_callback(batch)
                k += 1
            # Stop acquisition
            dig.cmd.DISARMACQUISITION()
            print("Stopping Acquisition...")
        if self.event_dump_callback:
            batch = all_detect
            all_detect = []
            self.event_dump_callback(batch)
        return all_detect
    
    def stop(self):
        self._stop_requested = True
    
    # =======================================================================
    # Acquisition helper methods
    # =======================================================================
    
    def _setup_digitizer(self, dig, acquisition_config: AcquisitionConfig):
        digitizer_channels: List[CaenDT5781Channel] = acquisition_config.digitizer.channels
        
        # Reset
        dig.cmd.RESET()
        
        # Get board info
        n_analog_traces = int(dig.par.NUMANALOGTRACES.value)
        adc_samplrate_msps = float(dig.par.ADC_SAMPLRATE.value)  # in Msps
        sampling_period_ns = int(1e3 / adc_samplrate_msps)
        fw_type = dig.par.FWTYPE.value
        
        # Configure digitizer
        dig.par.RECLEN.value        = str(digitizer_channels[0].rdc_len)
        dig.par.TRG_SW_ENABLE.value = 'TRUE'  # Enable software triggers_board parameter
        dig.par.STARTMODE.value     = 'START_MODE_SW'  # Set software start mode_board parameter
        dig.par.WAVEFORMS.value     = 'TRUE'  # Enable waveforms
        # Set channel parameters
        for i, ch in enumerate(dig.ch): # TODO: Make Definition for CH_ENABLED + add to parameter GUI
            ch.par.CH_ENABLED.value = 'TRUE' if digitizer_channels[i].enabled else 'FALSE'
        for i, channel in enumerate(digitizer_channels):
            chX = dig.get_node(f"/ch/{i}/par/")
            for field_name, digitizer_name in channel.iter_digitizer_definitions():
                if digitizer_name == "RECLEN": continue
                node = chX.get_node('/'+digitizer_name)
                node.value = str(channel.get_field_value(field_name))
        
        dig.cmd.CALIBRATEADC()
        
        # Compute record length in samples
        reclen_ns = int(dig.par.RECLEN.value)  # Read back RECLEN to check if there have been rounding
        reclen = int(reclen_ns / sampling_period_ns)
        
        # Configure probe types
        analog_probe_1_node = dig.vtrace[0]
        analog_probe_1_node.par.VTRACE_PROBE.value = 'VPROBE_INPUT'
        digital_probe_1_node = dig.vtrace[n_analog_traces + 0]
        digital_probe_1_node.par.VTRACE_PROBE.value = 'VPROBE_TRIGGER'
        
        # Configure endpoint
        data_format = [
            {
                'name': 'CHANNEL',
                'type': 'U8',
                'dim' : 0
            },
            {
                'name': 'FLAGS',
                'type': 'U32',
                'dim': 0
            },
            {
                'name': 'TIMESTAMP',
                'type': 'U64',
                'dim': 0,
            },
            {
                'name': 'ENERGY',
                'type': 'U16',
                'dim': 0,
            },
            {
                'name': 'ANALOG_PROBE_1',
                'type': 'I16',
                'dim': 1,
                'shape': [reclen]
            },
            {
                'name': 'ANALOG_PROBE_1_TYPE',
                'type': 'I32',
                'dim': 0
            },
            {
                'name': 'DIGITAL_PROBE_1',
                'type': 'U8',
                'dim': 1,
                'shape': [reclen]
            },
            {
                'name': 'DIGITAL_PROBE_1_TYPE',
                'type': 'I32',
                'dim': 0
            },
            {
                'name': 'WAVEFORM_SIZE',
                'type': 'SIZE_T',
                'dim': 0
            },
        ]
        decoded_endpoint_path = fw_type.replace('-', '')  # decoded endpoint path is just firmware type without -
        endpoint = dig.endpoint[decoded_endpoint_path]
        data = endpoint.set_read_data_format(data_format)
        return data, endpoint
    
    # =======================================================================
    # Supporter methods
    # =======================================================================
    
    def _make_uri(self) -> str:
        # Inspired from the start of demo_dpp.py at https://github.com/caenspa/py-caen-felib/tree/master
        ### CONNECTION PARAMETERS ###
        connection_type = 'usb'
        link_number = 0
        conet_node = 0
        vme_base_address = 0
        #############################
        
        dig1_scheme = 'dig1'
        dig1_authority = 'caen.internal'
        dig1_query = f'link_num={link_number}&conet_node={conet_node}&vme_base_address={vme_base_address}'
        dig1_path = connection_type
        return f'{dig1_scheme}://{dig1_authority}/{dig1_path}?{dig1_query}'
    
    def _can_use_digitizer(self) -> bool:
        return True
    
    def _cleanup(self):
        pass