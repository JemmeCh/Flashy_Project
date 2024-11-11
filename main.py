'''
Projet PHY3030 - FLASHy 

Programme d'analyse de pulse pour traitement FLASH 
à l'aide d'un BCT et d'un digitezer CAEN DT5781.

Ce fichier Python est le controlleur du projet, soit le lien entre l'analyse
et le GUI. 
'''
# TODO IN PART 2 OF PROJECT
# Use pickle library for reading binary file from digitizer

# Most imports in all the files
#import csv
#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('TkAgg')
#from scipy.integrate import trapezoid

#from typing import Final, List

#from Application import Application
from Controller.Controller import Controller
from Controller.ViewController import ViewController
from Controller.ModelController import ModelController


def main() -> None:
    view_controller = ViewController()
    model_controller = ModelController()
    main_controller = Controller(view_controller, model_controller)
    
    # Set up the links between the controllers
    model_controller.set_up(main_controller)
    view_controller.set_up(main_controller, "0.6")
    
    # Start program
    view_controller.mainloop()
    
   
if __name__ == '__main__':
    main()
    