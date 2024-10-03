'''
Projet PHY3030 - FLASHy 

Programme d'analyse de pulse pour traitement FLASH 
à l'aide d'un BCT et d'un digitezer CAEN DT5781.
'''
import csv
import numpy as np
import matplotlib.pyplot as plt

from typing import Final

#import Pulse

"""
Reads a CSV file from CoMPASS named file_name. The file comes from 
'{project-name}\DAQ\{Run-ID_increment}\RAW'.
Note: Register this dialect before using
csv.register_dialect("CoMPASS", delimiter=';')

TODO: Use watchdog to find that file automatically

Returns:
    [np.array]: np.array of each pulse
""" 
def readData(file_name:str) -> []:
    data = []
    
    with open(file_name, newline='') as f:
        reader = csv.reader(f, dialect='CoMPASS')
        # Skip header :
        # ['BOARD;CHANNEL;TIMETAG;ENERGY;CALIB_ENERGY;FLAGS;PROBE_CODE;SAMPLES']
        next(f)
        for row in reader:
            # Isolate SAMPLES
            row = np.array(row[7:], dtype=int)
            data.append(row)

    return data

def main() -> None:
    # TODO: Make it user chosen
    RECORD_LENGTH = 15000 #ns
    PRE_TRIGGER = 5000 #ns
    
    # CONSTANTS & SETTINGS
    csv.register_dialect("CoMPASS", delimiter=';')
    
    # START
    data = readData('SDataR_20240516_2.CSV')
    SAMPLE_SIZE: Final[int] = data[0].size
    STEPS: Final[int] = RECORD_LENGTH / SAMPLE_SIZE #ns
    
    t_axis = np.arange(0, RECORD_LENGTH, STEPS)
    
    first_element = data[0]
    #x_axis = np.linspace(1,first_element.size,num=first_element.size)
    plt.plot(t_axis, first_element)
    plt.show()
    
    
if __name__ == '__main__':
    main()
    