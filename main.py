'''
Projet PHY3030 - FLASHy 

Programme d'analyse de pulse pour traitement FLASH 
à l'aide d'un BCT et d'un digitezer CAEN DT5781.
'''
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid

import sys
import tkinter as tk
from tkinter import filedialog

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
def readData(file_name:str):
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

    array = np.array(data)
    
    return array

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
    
    for pulse in data:
        # Bring values close to zero
        hist, bin_edges = np.histogram(pulse, bins=50) # Adjust bins
        mode_value = bin_edges[np.argmax(hist)]
        leveled_pulse = pulse - mode_value
        
        # Find a threshold
        std_dev = np.std(leveled_pulse[np.abs(leveled_pulse) < 3 * np.std(leveled_pulse)])
        threshold = 0.60 * std_dev # Adjust value
        
        leveled_pulse[np.abs(leveled_pulse < threshold)] = 0
        levelData.append(leveled_pulse)
    
    return levelData

def levelData2(data):
    result = []
    threshold = 0.001
    
    # sous = np.median(data[:,:200], axis=0) moyenne par pulse (verifier axis)
    # (data.T - sous).T
    # switch = data >= threshold
    # data = data * switch 
    for pulse in data:
        # Median of the first 200 samples
        baseline = np.median(pulse[:200])
        leveled_pulse = pulse - baseline
        leveled_pulse[np.abs(leveled_pulse) < threshold] = 0 # y = y[y > sigma]
        
        result.append(leveled_pulse)
    return result

def areaUnderCurve(data:List[np.ndarray], x_axis) -> List[np.ndarray]:
    return [trapezoid(pulse, x_axis) for pulse in data]
    
def select_file() -> str:
    # REMOVE THIS AS SOON AS YOU ADD MORE
    root = tk.Tk()
    root.withdraw()
    # REMOVE THIS AS SOON AS YOU ADD MORE
    
    file_path = filedialog.askopenfilename(
        title="Select the CSV file to analyse",
        filetypes=(("CSV", "*.csv"), ("All files", "*.*"))
    )
    if not file_path:
        sys.exit()
    return file_path

def main() -> None:
    # TODO: Make it user chosen
    RECORD_LENGTH = 15000 #ns
    PRE_TRIGGER = 5000 #ns
    
    # CONSTANTS & SETTINGS
    csv.register_dialect("CoMPASS", delimiter=';')
    
    # START
    file_path = "SDataR_20240516_2.CSV"#select_file()
    
    data = readData(file_path)
    data = [pulse / 10000 for pulse in data]
    SAMPLE_SIZE: Final[int] = data[0].size
    t_axis, dt = np.linspace(0, RECORD_LENGTH / 1000, SAMPLE_SIZE, retstep=True)
    
    print(data, "\n")
    
    data = levelData2(data)
    
    print(data)
    print(data[0].tolist())
    
    graphData(data, t_axis)
    
    #print(areaUnderCurve(data, t_axis))
    
    
if __name__ == '__main__':
    main()
    