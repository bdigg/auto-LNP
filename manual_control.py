import sys
from email.header import UTF8
sys.path.append('./DLL64')
sys.path.append('./Elveflow64.py')
from ctypes import *
from array import array
from Elveflow64 import *
import time
import matplotlib.pyplot as plt
import pressure as pump

Instr_ID = c_int32()

#----------------------------------Parameters-----------------------------------
inst_name = '01EA53FD'
#Sensor setup [Channel, Type (5-1000uL/min)(4-80uL/min) , Digital (1), Calibration (H20 -0), Pixel (7) ]
sensor1 = [1,4,1,0]
sensor2 = None #[2,5,1,0]
sensor3 = None #[3,5,1,0]
sensor4 = None #[4,5,1,0]
#Pressure calibrate
pressure_calibrate = "default"

#Flow rates of each input channel
experiments = [[50,None,None,None],[50,None,None,None]]

#Repeats
standard_repeats = 1 #How many tines should each composition be repeated
fail_repeats = 1 #If FR falls out of range, how many repeats 

#PI Controller Parameters
K_p = 0.05 #Tune the proportioal component
K_i = 0.1 #Tune the integral component 
p_range = [0,80] #min,max

#Experiment timings
max_equilibration_t = 40 #Maximum time to reach FR equilibrium
experiment_t = 20 # 

#----------------------------------Initiation-----------------------------------
pump.pressure_init()
pump.sensor_init(sensor1, sensor2, sensor3, sensor4)
pump.pressure_calib(pressure_calibrate)
#---------------------------------Main Loop------------------------------------
K_p = 0.05
K_i = 0.1
p_range = [0,80] #min,max

max_equilibration_t = 40
experiment_t = 20

#Run Experiments
for FR in experiments:
    repeats = 0   
    while repeats < standard_repeats:
        collection,consistent_fr = pump.main_PI(K_p,K_i,FR,experiment_t,max_equilibration_t)
        if consistent_fr == False:
            repeats += -1
        repeats += 1