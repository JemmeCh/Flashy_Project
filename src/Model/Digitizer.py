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
            
            # Set adc_n_bits for the analysers
            self.controller.set_ADC_NBIT(adc_n_bits)
            
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
        return
    
    def arm_digitizer(self):
        """Useless"""
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

    def _on_close_plot(self, event):
        # When closing oonline plot, has the same effect of clicking the button
        self.controller.view_controller.bypass.data_aqc_panel.record_button.stop_recording()
    
    def record_data(self):
        # Check if the digitizer has been connected
        if not self.model_controller.controller.hasDIGITIZERCONNECTED and self.ping_digitizer():
            self.send_feedback("There is no digitizer connected")
            self.controller.view_controller.bypass.data_aqc_panel.record_button.stop_recording()
            return
        # Check if the digitizer can be used
        if not self.model_controller.controller.can_use_dig():
            self.send_feedback("The digitizer is being used!")
            self.controller.view_controller.bypass.data_aqc_panel.record_button.stop_recording()
            return
        
        self.controller.isRECORDING = True
        self.send_feedback("Digitizer can be used! Fetching paramters...")
        dig_parameters = self.controller.get_dig_parameters() # Contains all parameters
        CH0_parameters   : Dict[str, str] = {}
        CH1_parameters   : Dict[str, str] = {}
        for parameter in dig_parameters.values():
            state = parameter.get_state()
            if parameter.get_name() == 'Record Lenght (ns)':
                continue
            match state:
                case 'board':
                    value = (parameter.get_row()[1])
                    dig_name = parameter.get_dig_name()
                    CH0_parameters[dig_name] = value
                    CH1_parameters[dig_name] = value
                case 'CH0':
                    value = (parameter.get_row()[2])
                    dig_name = parameter.get_dig_name()
                    CH0_parameters[dig_name] = value
                case 'CH1':
                    value = (parameter.get_row()[3])
                    dig_name = parameter.get_dig_name()
                    CH1_parameters[dig_name] = value
                case _:
                    continue
        
        self.send_feedback("Parameters fetched! Connecting to digitizer...")
        with device.connect(self.uri) as dig:
            self.send_feedback("Connected! Configurating parameters")
            # Reset
            dig.cmd.RESET()
            
            # Get board info
            n_analog_traces = int(dig.par.NUMANALOGTRACES.value)
            n_digital_traces = int(dig.par.NUMDIGITALTRACES.value)
            adc_samplrate_msps = float(dig.par.ADC_SAMPLRATE.value)  # in Msps
            adc_n_bits = int(dig.par.ADC_NBIT.value)
            sampling_period_ns = int(1e3 / adc_samplrate_msps)
            fw_type = dig.par.FWTYPE.value

            # Configure digitizer
            dig.par.RECLEN.value        = dig_parameters['Record Lenght (ns)'].get_row()[1]
            dig.par.TRG_SW_ENABLE.value = 'TRUE'  # Enable software triggers_board parameter
            dig.par.STARTMODE.value     = 'START_MODE_SW'  # Set software start mode_board parameter
            dig.par.WAVEFORMS.value     = 'TRUE'  # Enable waveforms
            # Set channel parameters
            for i, ch in enumerate(dig.ch):
                # Enable only channel 0. In the future (if you need to use both or the other channel,
                # this is what you have to change)
                ch.par.CH_ENABLED.value      =  'TRUE' if i == 0 else 'FALSE'
            
            ch0 = dig.get_node("/ch/0/par/")
            ch1 = dig.get_node("/ch/1/par/")
            for dig_name, value in CH0_parameters.items():
                node = ch0.get_node('/'+dig_name)
                node.value = str(value)
            for dig_name, value in CH1_parameters.items():
                node = ch1.get_node('/'+dig_name)
                node.value = str(value)
                        
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

            self.send_feedback("Digitizer configured! Setting up online plot...")
            
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
            
            # Configure plot
            plt.ion()
            figure, ax = plt.subplots(figsize=(5, 4))
            lines = []
            for i in range(2):
                line, = ax.plot([], [])
                lines.append(line)
            ax.set_xlim(0, reclen - 1)
            ax.set_ylim(0, 2 ** adc_n_bits - 1)  
            figure.canvas.mpl_connect('close_event', self._on_close_plot)
                      
            # Start acquisition
            dig.cmd.ARMACQUISITION()
            k = 1
            
            # Save file as running
            all_detect = []
            
            self.send_feedback("Plot set! Starting Acquisition...")
            while self.controller.isRECORDING:
                dig.cmd.SENDSWTRIGGER()
                try:
                    endpoint.read_data(10,data)
                    all_detect.append([ # We don't use the other values 
                        channel.copy(), flags.copy(),
                        waveform_size.copy(), analog_probe_1.copy()
                    ])
                    if np.mean(analog_probe_1) > 2500:
                        self.send_feedback(f"Pulse detected! {k}")
                        k += 1
                
                except error.Error as ex:
                    if ex.code == error.ErrorCode.TIMEOUT:
                        continue
                    elif ex.code == error.ErrorCode.STOP:
                        break
                    else:
                        raise ex
                        
                assert analog_probe_1_type == 1  # 1 -> 'VPROBE_INPUT'
                assert digital_probe_1_type == 26  # 26 -> 'VPROBE_TRIGGER'
                valid_sample_range = np.arange(0, waveform_size)
                lines[0].set_data(valid_sample_range, analog_probe_1)
                lines[1].set_data(valid_sample_range, digital_probe_1.astype(np.int64) * 2000)  # scale digital probe to be visible

                ax.title.set_text(f'Channel: {channel} Timestamp: {timestamp} Energy: {energy}')

                figure.canvas.draw()
                figure.canvas.flush_events()
            
            # Stop acquisition
            dig.cmd.DISARMACQUISITION()
            self.send_feedback("Stopping Acquisition...")
            
            # Save data and continue process
            self.controller.post_acquisition(all_detect)
        return