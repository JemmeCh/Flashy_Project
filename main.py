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
from scipy.integrate import trapezoid

from typing import Final, List

from Application import Application

csv.register_dialect("CoMPASS", delimiter=';')
matplotlib.use('TkAgg')

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

def levelData(data:np.ndarray):
    threshold = 8

    # Calculate de median of each pulse
    sous = np.median(data[:, :200], axis=1)
    # Bring values close to zero
    data = (data.T - sous).T
    # Bring value to zero if lower than threshold
    data[np.abs(data) < threshold] = 0
    return data
    
def areaUnderCurve(data:np.ndarray, x_axis, dx) -> np.ndarray:
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
    


    
if __name__ == '__main__':
    main()
    