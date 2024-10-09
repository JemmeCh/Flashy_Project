'''
Projet PHY3030 - FLASHy 

Programme d'analyse de pulse pour traitement FLASH 
à l'aide d'un BCT et d'un digitezer CAEN DT5781.

Ce fichier Python est le controlleur du projet, soit le lien entre l'analyse
et le GUI. 
'''
# TODO IN PART 2 OF PROJECT
# Use pickle library for reading binary file from digitizer

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from scipy.integrate import trapezoid

from typing import Final, List

from Application import Application
from time import time

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

def graphData(data:np.ndarray, t_axis):
    # TODO: Make it for the future pulse list thing (yk what you mean)
    plt.figure(figsize=(10,6))
    for pulse in data:
        plt.plot(t_axis, pulse)
    
    plt.grid(True)
    plt.xlabel("Temps (microseconde)")
    plt.ylabel("Tension (V)")
    plt.show()

def levelData(data:np.ndarray) -> np.ndarray:
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
    
    return np.array(levelData)

def levelData2(data:np.ndarray) -> np.ndarray:
    result = []
    threshold = 8
     
    for pulse in data:
        # Median of the first 200 samples
        baseline = np.median(pulse[:200])
        leveled_pulse = pulse - baseline
        leveled_pulse[np.abs(leveled_pulse) < threshold] = 0
        
        result.append(leveled_pulse)
    return np.array(result)

def levelData3(data:np.ndarray):
    threshold = 8

    # Calculate de median of each pulse
    sous = np.median(data[:, :200], axis=1)
    # Bring values close to zero
    data = (data.T - sous).T
    # Bring value to zero if lower than threshold
    data[np.abs(data) < threshold] = 0
    return data

def areaUnderCurve(data:List[np.ndarray], x_axis, dt) -> np.ndarray:
    return np.array([trapezoid(pulse, x_axis) for pulse in data])
    
def areaUnderCurve2(data:np.ndarray, x_axis, dx) -> np.ndarray:
    # Trapezoid method with matrices
    left = data[:,  :-1]
    right = data[:, 1:  ]
    
    # Creating the switch to check if we're below x=0
    lswitch = left  >= 0
    rswitch = right >= 0 
    switch = ~(lswitch & rswitch)
   
    # Calculating the area under each trapezoid
    # The minus is if the curve is below x=0
    area = (np.abs(left) + np.abs(right)) * dx / 2 \
           - ( switch.astype(int) * (np.abs(left) + np.abs(right)) * dx)
    
    return np.sum(area, axis=1)

def main() -> None:
    # TODO: Make it user chosen
    RECORD_LENGTH = 15000 #ns
    PRE_TRIGGER = 5000 #ns
    
    app = Application()
    data = readData("SDataR_20240516_2.CSV")
    #data = np.array([pulse / 10000 for pulse in data])
    SAMPLE_SIZE: Final[int] = data[0].size
    t_axis, dt = np.linspace(0, RECORD_LENGTH / 1000, SAMPLE_SIZE, retstep=True)

    #print(data, "\n")
    
    #testLevelingFunc(data, t_axis)
    #testAreaFunc(data, t_axis, dt)
    
    #graphData(data, t_axis)
    
    #print(areaUnderCurve(data, t_axis))
    app.mainloop()
    
    
def testAreaFunc(data:np.ndarray, t_axis, dt):
    data1 = levelData3(data.copy())
    data2 = levelData3(data.copy())
    
    start = time()
    data1 = areaUnderCurve(data1, t_axis, dt)
    end = time()
    print(f"Utilisant fonction 1: {end - start}")
    start = time()
    data2 = areaUnderCurve2(data2, t_axis, dt)
    end = time()
    print(f"Utilisant fonction 2: {end - start}")
    
    """ print("Data1 =")
    print(data1)
    print("Data2 =")
    print(data2) """
    
def testLevelingFunc(data:np.ndarray, t_axis):
    data1 = data.copy()
    data2 = data.copy()
    data3 = data.copy()
    
    start = time()
    data1 = levelData(data1)
    end = time()
    print(f"Utilisant fonction 1: {end - start}")
    start = time()
    data2 = levelData2(data2)
    end = time()
    print(f"Utilisant fonction 2: {end - start}")
    start = time()
    data3 = levelData3(data3)
    end = time()
    print(f"Utilisant fonction 3: {end - start}")
    
    print("Data1 =")
    print(data1[0].tolist())
    print("Data2 =")
    print(data2[0].tolist())
    print("Data3 =")
    print(data3[0].tolist())
    
    graphData(data1, t_axis)
    graphData(data2, t_axis)
    graphData(data3, t_axis)
    
    #print((data2[0] == data3[0]).tolist())

    
if __name__ == '__main__':
    main()
    