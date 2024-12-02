import numpy as np
from typing import TYPE_CHECKING, Any, Dict

import matplotlib.pyplot as plt
from src.Model.Error import Error

# To install the module: pip install caen-felib
from caen_felib import lib, device, error

print(f'CAEN FELib wrapper loaded (lib version {lib.version})')

if TYPE_CHECKING:
    from Controller.ModelController import ModelController
    from Controller.Controller import Parameter
   
class Digitizer:
    def __init__(self, model_controller:"ModelController"):
        self.model_controller = model_controller
        self.data_analyser = model_controller.get_data_analyser()
        
        # Getting access to useful stuff
        self.send_feedback = model_controller.send_feedback
        self.dispatch_data = model_controller.dispatch_data
        self.change_aqc_panel_status = model_controller.change_aqc_panel_status
        self.error_handling = model_controller.controller.error_handling
        
        # Defining error handling
        self.get_basic_dig_info = self.error_handling.handle_CAEN_exceptions(self.get_basic_dig_info)
        self.arm_digitizer = self.error_handling.handle_CAEN_exceptions(self.arm_digitizer)
        self.record_data = self.error_handling.handle_CAEN_exceptions(self.record_data)
        
        # Make uri for accessing digitizer
        self.make_uri()
        
        # isRECORDING access
        self.controller = model_controller.controller
    
    def make_uri(self):
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
        self.uri = f'{dig1_scheme}://{dig1_authority}/{dig1_path}?{dig1_query}'

    def ping_digitizer(self):
        try:
            with device.connect(self.uri):
                return False
        except Exception:
            self.model_controller.controller.hasDIGITIZERCONNECTED = False
            self.model_controller.controller.change_aqc_panel_status('Déconnecté')
            return True
       
    def get_basic_dig_info(self):
        # Check if the digitizer can be used
        if not self.model_controller.controller.can_use_dig():
            self.send_feedback("The digitizer is being used!")
            return
        if self.ping_digitizer():
            self.send_feedback("Couldn't connect to digitizer!")
        self.send_feedback("Attempting to connect to digitizer...")
        """ test_data = {
                    'model_name': 'name',
                    'family_code': 'familycode',
                    'fw_type': 'fw_type',
                    'serial_num': 1234,
                    'adc_n_bits': 12,
                    'adc_samplrate_msps': 1000,
                    'sampling_period_ns': 10,
                    'max_rawdata_size': 9000
                }
        self.dispatch_data(test_data) """
        #print(self.uri)
        with device.connect(self.uri) as dig:
            self.send_feedback("Digitizer connected! Retreiving basic info...")
            self.model_controller.controller.isGETTING_BASIC_INFO = True
            # Change status
            self.change_aqc_panel_status("Connecté")
            
            # First connection
            self.model_controller.controller.hasDIGITIZERCONNECTED = True
            
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
            
            # Pack information
            data = {
                'model_name': name,
                'family_code': familycode,
                'fw_type': fw_type,
                'serial_num': serial_num,
                'adc_n_bits': adc_n_bits,
                'adc_samplrate_msps': adc_samplrate_msps,
                'sampling_period_ns': sampling_period_ns,
                'max_rawdata_size': max_rawdata_size
            }
            
            # Send info to panel
            self.dispatch_data(data)
            
            # Close digitizer
            self.model_controller.controller.isGETTING_BASIC_INFO = False
            self.send_feedback("Info retreived successfully!")
    
    def arm_digitizer(self):
        # Check if the digitizer has been connected
        if not self.model_controller.controller.hasDIGITIZERCONNECTED:
            self.send_feedback("There is no digitizer connected!")
            return
        # Check if the digitizer can be used
        if not self.model_controller.controller.can_use_dig():
            self.send_feedback("The digitizer is being used!")
            return
        
        self.send_feedback("Attempting to arm the digitizer...")
        
        #TODO: The check box will make the record data click-able
        
        with device.connect(self.uri):
            self.send_feedback("I dont really understand how this would works... Im currently reseting the board every time data is being recorded")
            
    def record_data(self):
        # Check if the digitizer has been connected
        """ if not self.model_controller.controller.hasDIGITIZERCONNECTED and self.ping_digitizer():
            self.send_feedback("There is no digitizer connected")
            self.controller.view_controller.bypass.data_aqc_panel.record_button.stop_recording()
            return """
        # Check if the digitizer can be used
        if not self.model_controller.controller.can_use_dig():
            self.send_feedback("The digitizer is being used!")
            self.controller.view_controller.bypass.data_aqc_panel.record_button.stop_recording()
            return
        self.controller.isRECORDING = True
        self.send_feedback("Digitizer can be used! Fetching paramters...")
        dig_parameters = self.controller.get_dig_parameters()
        # get_parameter() returns [value for board, value for CH0, value for CH1, state]
        """PLEASE GO THINK ABOUT THIS CAUSE WTF"""
        board_parameters : Dict[str, "Parameter"] = {}
        CH0_parameters   : Dict[str, "Parameter"] = {}
        CH1_parameters   : Dict[str, "Parameter"] = {}
        for parameter in dig_parameters.values():
            state = parameter.get_state()
            match state:
                case 'board':
                    board_parameters[parameter.get_name()] = parameter
                case 'CH0':
                    CH0_parameters.update((parameter.get_name(), parameter))
                case 'CH1':
                    CH1_parameters.update((parameter.get_name(), parameter))
            
        with device.connect(self.uri) as dig:
            # Reset
            dig.cmd.RESET()
            
            # Get board info
            n_ch = int(dig.par.NUMCH.value)
            adc_samplrate_msps = float(dig.par.ADC_SAMPLRATE.value)
            sampling_period_ns = int(1e3 / adc_samplrate_msps)
            fw_type = dig.par.FWTYPE.value
            n_analog_traces = int(dig.par.NUMANALOGTRACES.value) # new
            n_digital_traces = int(dig.par.NUMDIGITALTRACES.value) # new
            
            # Configuration parameters
            # TODO: Make them user chosen
            reclen_ns = 15000
            pretrg_ns = 5000
            
            # Configure digitizer
            dig.par.RECLEN.value = f'{reclen_ns}'
            dig.par.TRG_SW_ENABLE.value = 'TRUE'  # Enable software triggers_board parameter
            dig.par.STARTMODE.value = 'START_MODE_SW'  # Set software start mode_board parameter
            dig.par.WAVEFORMS.value = 'TRUE'  # Enable waveforms
            for i, ch in enumerate(dig.ch):
                ch.par.CH_ENABLED.value = 'TRUE' if i == 0 else 'FALSE'  # Enable only channel 0
                ch.par.CH_PRETRG.value = f'{pretrg_ns}' if i == 0 else '2000'

            dig.cmd.CALIBRATEADC()
            
            # Compute record length in samples
            reclen_ns = int(dig.par.RECLEN.value)  # Read back RECLEN to check if there have been rounding
            reclen = int(reclen_ns / sampling_period_ns)
            
            # Configure probe types (new)
            analog_probe_1_node = dig.vtrace[0]
            analog_probe_1_node.par.VTRACE_PROBE.value = 'VPROBE_INPUT'
            digital_probe_1_node = dig.vtrace[n_analog_traces + 0]
            digital_probe_1_node.par.VTRACE_PROBE.value = 'VPROBE_TRIGGER'
            
            # Configure endpoints
            data_format_probe = [
                {
                    'name': 'CHANNEL',
                    'type': 'U8',
                    'dim' : 0
                },
                {
                    'name': 'WAVEFORM_SIZE', # This gives the amount of samples
                    'type': 'SIZE_T',
                    'dim': 0
                },
                {
                    'name': 'TIMESTAMP_NS', # No ns is TIMESTAMP
                    'type': 'DOUBLE', # U64
                }, # Idea one: use probing to see if it gets me the samples
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
            ]
            '''{ Not supported on dpp-pha software
                    'name': 'WAVEFORM',
                    'type': 'U16',
                    'dim': 2,
                    'shape': [n_ch, reclen],
                },'''
                
            data_format_raw = [
                {
                    "name": "DATA",
                    "type": "U8",
                    "dim": 1,
                    "shape": [reclen]
                },
                {
                    "name": "SIZE",
                    "type": "SIZE_T",
                    "dim": 0
                }
            ]
            decoded_endpoints_path = fw_type.replace('-', '')
            endpoint_probe = dig.endpoint[decoded_endpoints_path] # Try dig.endpoint['raw']
            data_probe = endpoint_probe.set_read_data_format(data_format_probe)
            
            endpoint_raw = dig.endpoint['raw']
            data_raw = endpoint_raw.set_read_data_format(data_format_raw)
            
            """  # Get reference to data fields
            channel = data_probe[0].value
            waveform_size = data_probe[1].value
            timestamp = data_probe[2].value
            analog_probe_1 = data_probe[3].value
            analog_probe_1_type = data_probe[4].value  # Integer value described in Supported Endpoints > Probe type meaning
            digital_probe_1 = data_probe[5].value
            digital_probe_1_type = data_probe[6].value  # Integer value described in Supported Endpoints > Probe type meaning
             """
            # Raw data collection activation
            dig.endpoint.par.activeendpoint.value = 'raw'  
                      
            # Start acquisition
            dig.cmd.ARMACQUISITION()
            self.send_feedback("Starting Acquisition...")
            while self.controller.isRECORDING:
                dig.cmd.SENDSWTRIGGER()
                try:
                    #endpoint_probe.read_data(10, data_probe)
                    endpoint_raw.read_data(10, data_probe)
                except error.Error as ex:
                    if ex.code == error.ErrorCode.TIMEOUT:
                        continue
                    elif ex.code == error.ErrorCode.STOP:
                        break
                    else:
                        raise ex
            
            # Stop acquisition
            dig.cmd.DISARMACQUISITION()
            self.send_feedback("Stopping Acquisition...")
            
            for i in data_probe:
                print(i)
            #print(data_raw)
            
            # Send data to be analyzed by DataAnalyser
            self.send_feedback("Sending data to analyser...")
            self.data_analyser.analyse_dig_data(data_raw, n_ch)