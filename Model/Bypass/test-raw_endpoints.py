import numpy as np
from caen_felib import lib, device, error
import keyboard
import time
import pickle

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
dig1_uri = f'{dig1_scheme}://{dig1_authority}/{dig1_path}?{dig1_query}'

with device.connect(dig1_uri) as dig: 
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
        },
    ]
    endpoint_raw = dig.endpoint['raw']
    data_raw = endpoint_raw.set_read_data_format(data_format_raw)
    # Raw data collection activation
    dig.endpoint.par.activeendpoint.value = 'raw'
        
    # Start acquisition
    dig.cmd.ARMACQUISITION()
    print("armed")
    k = 1
    running = True
    
    # Save file as running
    time = time.asctime(time.localtime()).replace(' ','-')
    time = time.replace(':','_')
    name_file = f"test-raw_endpoints-{time}.dat"
    file = open(name_file, "wb")
    
    while running:
        if keyboard.is_pressed('q'):  # Check if 'q' key is pressed
            print("You pressed 'q'. Exiting loop...")
            running = False  # Set the running condition to False
            
        dig.cmd.SENDSWTRIGGER()
        try:    
            pickle.dump(endpoint_raw.read_data(10, data_raw), file)
        except error.Error as ex:
            if ex.code == error.ErrorCode.TIMEOUT:
                print('continue')
                continue
            elif ex.code == error.ErrorCode.STOP:
                print("break")
                break
            else:
                raise ex
    
    # Stop acquisition
    dig.cmd.DISARMACQUISITION()
    file.close()