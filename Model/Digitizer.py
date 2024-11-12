import numpy as np
from typing import TYPE_CHECKING, Any, Dict

from Model.Error import Error

# To install the module: pip install caen-felib
from caen_felib import lib, device, error

print(f'CAEN FELib wrapper loaded (lib version {lib.version})')

if TYPE_CHECKING:
    from Controller.ModelController import ModelController
   
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
       
    def get_basic_dig_info(self):
        # Check if the digitizer can be used
        if not self.model_controller.controller.can_use_dig():
            self.send_feedback("The digitizer is being used!")
            return
        
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
        self.dig_info_panel.dispatch_data(test_data) """
        #print(self.uri)
        with device.connect(self.uri) as dig:
            self.send_feedback("Digitizer connected! Retreiving basic info...")
            self.model_controller.controller.isGETTING_BASIC_INFO = True
            # Change status
            self.change_aqc_panel_status("Connecté")
            
            # First connection
            self.model_controller.controller.hasDIGITIZERCONNECTED = True
            # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO 
            # Make it so the program detects when digitizer is unpluged
            
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
        if not self.model_controller.controller.hasDIGITIZERCONNECTED:
            self.send_feedback("There is no digitizer connected")
            self.controller.view_controller.bypass.data_aqc_panel.record_button.stop_recording()
            return
        # Check if the digitizer can be used
        if not self.model_controller.controller.can_use_dig():
            self.send_feedback("The digitizer is being used!")
            self.controller.view_controller.bypass.data_aqc_panel.record_button.stop_recording()
            return
        
        with device.connect(self.uri) as dig:
            self.controller.isRECORDING = True
            # Reset
            dig.cmd.RESET()
            
            # Get board info
            n_ch = int(dig.par.NUMCH.value)
            adc_samplrate_msps = float(dig.par.ADC_SAMPLRATE.value)
            sampling_period_ns = int(1e3 / adc_samplrate_msps)
            fw_type = dig.par.FWTYPE.value
            
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
            
            # Configure endpoints
            data_format = [
                {
                    'name': 'EVENT_SIZE',
                    'type': 'SIZE_T',
                },
                {
                    'name': 'TIMESTAMP',
                    'type': 'U64',
                },
                {
                    'name': 'WAVEFORM_SIZE', # This gives the amount of samples
                    'type': 'SIZE_T',
                    'dim': 0
                },
                {
                    'name': 'WAVEFORM', # Supposed to give the samples doesnt work lol
                    'type': 'U16',
                    'dim': 2,
                    'shape': [n_ch, reclen],
                },
            ]
            decoded_endpoints_path = fw_type.replace('-', '')
            endpoint = dig.endpoint[decoded_endpoints_path] # Try dig.endpoint['raw']
            data = endpoint.set_read_data_format(data_format)
            
            # Get reference to data fields
            #event_size = data[0].value
            #timestamp = data[1].value
            #waveform = data[2].value
            #waveform_size = data[3].value
            
            # Start acquisition
            dig.cmd.ARMACQUISITION()
            
            while self.controller.isRECORDING:
                dig.cmd.SENDSWTRIGGER()
                try:
                    endpoint.read_data(10, data)
                except error.Error as ex:
                    if ex.code == error.ErrorCode.TIMEOUT:
                        continue
                    elif ex.code == error.ErrorCode.STOP:
                        break
                    else:
                        raise ex
            
            # Stop acquisition
            dig.cmd.disarmacquisition()
            
            # Send data to be analyzed by DataAnalyser
            self.send_feedback("Sending data to analyser...")
            self.data_analyser.analyse_dig_data(data, n_ch)