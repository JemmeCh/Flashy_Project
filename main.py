'''
Projet PHY3030 - FLASHy 

Programme d'analyse de pulse pour traitement FLASH 
à l'aide d'un BCT et d'un digitezer CAEN DT5781.
'''
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid

# TODO IN PART 2 OF PROJECT
# Use pickle library for reading binary file from digitizer

from typing import Final, List

"""
Reads a CSV file from CoMPASS named file_name. The file comes from 
\{project-name}\DAQ\{Run-ID_increment}\RAW.
Note: Register this dialect before using
csv.register_dialect("CoMPASS", delimiter=';')

TODO: Use watchdog to find that file automatically

Returns:
    [np.array]: np.array of each pulse
""" 
def readData(file_name:str) -> List[np.ndarray]:
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

def graphData(data:List[np.ndarray], t_axis):
    # TODO: Make it for the future pulse list thing (yk what you mean)
    plt.figure(figsize=(10,6))
    for pulse in data:
        plt.plot(t_axis, pulse)
    
    plt.grid(True)
    plt.xlabel("Temps (microseconde)")
    plt.ylabel("Tension (V)")
    plt.show()

def levelData(data:List[np.ndarray]) -> List[np.ndarray]:
    levelData = []
    
    for arr in data:
        # Bring values close to zero
        hist, bin_edges = np.histogram(arr, bins=50) # Adjust bins
        mode_value = bin_edges[np.argmax(hist)]
        leveled_arr = arr - mode_value
        
        # Find a threshold
        std_dev = np.std(leveled_arr[np.abs(leveled_arr) < 3 * np.std(leveled_arr)])
        threshold = 0.60 * std_dev # Adjust value
        
        leveled_arr[np.abs(leveled_arr < threshold)] = 0
        levelData.append(leveled_arr)

    # The data needs to be scaled down from 1000 to 0.1
    levelData = [pulse / 10000 for pulse in levelData]
    
    return levelData


def areaUnderCurve(data:List[np.ndarray], x_axis) -> List[np.ndarray]:
    return [trapezoid(pulse, x_axis) for pulse in data] # This is in nC
    

def main() -> None:
    # TODO: Make it user chosen
    RECORD_LENGTH = 15000 #ns
    PRE_TRIGGER = 5000 #ns
    
    # CONSTANTS & SETTINGS
    csv.register_dialect("CoMPASS", delimiter=';')
    
    # START
    data = readData('SDataR_20240516_2.CSV')
    SAMPLE_SIZE: Final[int] = data[0].size
    STEPS: Final[int] = int(RECORD_LENGTH / SAMPLE_SIZE) #ns
    t_axis = np.linspace(0, RECORD_LENGTH / 1000, num=data[0].size)
    
    data = levelData(data)
    
    graphData(data, t_axis)
    
    print(areaUnderCurve(data, t_axis))
    
    
if __name__ == '__main__':
    main()
    