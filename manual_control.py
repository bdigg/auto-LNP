import sys
import pandas as pd
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

#----------------------------------Experiment Parameters-----------------------------------
Mode = "Flow","Composition"


#----------------------------------Controller Parameters-----------------------------------
inst_name = '01EA53FD'
active_chans = [1,2] #Set all active channels
#Sensor setup [Channel, Type (5-1000uL/min)(4-80uL/min) , Digital (1), Calibration (H20 -0), Pixel (7) ]
sensor1 = [1,5,1,0]#[1,4,1,0]
sensor2 = [2,4,1,0]
sensor3 = [3,5,1,0]
sensor4 = None #[4,5,1,0]
#Pressure calibrate
pressure_calibrate = "default"

#Flow rates of each input channel
volume = 100 #volume produced in micro litres
experiments = [[50,50,None,None],[30,50,None,None]]

#Repeats
standard_repeats = 1 #How many tines should each composition be repeated
fail_repeats = 1 #If FR falls out of range, how many repeats 

#PI Controller Parameters
period = 0.4
K_p = 0.013 #Tune the proportioal component
K_i = 0.0005 #Tune the integral component 
p_range = [0,80] #min,max

#Experiment timings
max_equilibration_t = 120 #Maximum time to reach FR equilibrium
eq_duration = 15 #Time over which the FR must be stable
experiment_t = 30 # 

#----------------------------------Initiation-----------------------------------
pump.pressure_init()
pump.sensor_init(sensor1, sensor2, sensor3, sensor4)
pump.pressure_calib(pressure_calibrate)
#pump.flush(active_chans,100,(1*60))
pump.stability_test(active_chans,[20,40,80,100])
#K_p,K_i = pump.auto_tune(active_chans,period)
#---------------------------------Main Loop------------------------------------

print(pump.get_sensor_data(2))

#Run Experiments, repeating as specified 
for FR in experiments:
    repeats = 0   
    while repeats < standard_repeats:
        print("Beginning experiment: ", FR)
        collection,consistent_fr = pump.main_PI(period,K_p,K_i,FR,experiment_t,max_equilibration_t,eq_duration)
        if consistent_fr == False:
            repeats += -1
        repeats += 1
        control = input("Continue? (y)")
pump.stop()

#--------------------------------Functions------------------------------------------
