import sys
import pandas as pd
from email.header import UTF8
sys.path.append('./DLL64')
sys.path.append('./Elveflow64.py')
from ctypes import *
from array import array
from Elveflow64 import *
import time
import numpy as np
import matplotlib.pyplot as plt
import pump 
import control
import flow_calculator as calc
import expel
import threading
Instr_ID = c_int32()

#----------------------------------Experiment Parameters-----------------------------------
#Mode = "Composition"
Mode = "Flow"

if Mode == "Composition":
    #FRR
    FRR_range = range(1,10+1,1) #[min,max,increment]

    #Channel 1 - Buffer 
    Buffer = [True, range(180,180+1,20)]

    #Channel 2 - Lipid 1 in ethanol
    #Lp1=[Active?,Name, MW, Range , Concentration]  
    Lp1 = ["Lipid1_Name", 100, "Base",  10]  

    #Channel 3 - Lipid 2 in ethanol - if not active, set range to 0
    #Lp2= [Active?,Name, MW, Range , Concentration]  
    Lp2 = ["Lipid2_Name", 50, range(0,(10+1),5), 5]  

    #Channel 4 - Lipid 3 in ethanol - if not active, set range to 0
    #Lp3= [Name, MW, Range , Concentration]  
    Lp3 = ["Lipid3_Name", 50, range(0,(10+1),5), 5]   

    exp_params,exp_FRs = calc.flow_calc(FRR_range,Buffer,Lp1,Lp2,Lp3)
    print(exp_FRs)

elif Mode == "Flow":
    exp_FRs = [[50,40,0,0],[60,30,0,0],[70,20,0,0],[80,50,0,0],[100,40,0,0]]


#----------------------------------Controller Parameters-----------------------------------
inst_name = '01EA53FD'
active_chans = [1,2] #Set all active channels
#Sensor setup [Channel, Type (5-1000uL/min)(4-80uL/min) , Digital (1), Calibration (H20 -0), Pixel (7) ]
sensor1 = [1,5,1,0]#[1,4,1,0]
sensor2 = [2,5,1,0]  ##IMPORTANT Change calibration if using MFS3 sensor - control.py PID
sensor3 = None#[3,4,1,0]
sensor4 = None #[4,5,1,0]
#Pressure calibrate
pressure_calibrate = "default"

#Flow rates of each input channel#
volume = 20 #volume produced in micro litres

#Repeats
standard_repeats = 1 #How many tines should each composition be repeated
fail_repeats = 1 #If FR falls out of range, how many repeats 

#PI Controller Parameters
period = 0.2
K_p = [0.02,0.02] #Tune the proportioal component 0.018
K_i = 0.0001 #Tune the integral component  0.0005
p_incr = [-20,20] #min,max
p_range = [0,200] #min,max

#Experiment timings
max_equilibration_t = 300 #Maximum time to reach FR equilibrium
eq_duration = 5 #Time over which the FR must be stable



#Autocollect Configuration 
autocollect = True
wpdim = [8,12] #row col
wpcurrent = [1,1] #set this as the first well to be used
#add wp dimensions in mm etc for conversion


#----------------------------------Initiation-----------------------------------
error = 0 
while error == 0:
    if autocollect  == True:
        print("oi")
        global ser
        ser = expel.serconnect()
        threading.Thread(target=expel.homeandwaste,args=(ser)).start()
    error = pump.pressure_init()
    error = pump.sensor_init(sensor1, sensor2, sensor3, sensor4)
    #error = control.flush(active_chans,75,(1*30)) #pressure 
    #error = control.stability_test(active_chans,[20,40,80,100])
    #control.flowtable(active_chans,)
    #K_p,K_i = control.auto_tune(active_chans,period)
    #---------------------------------Main Loop------------------------------------
    main_loop = True

    if main_loop == True:
        control.main_PI(autocollect,active_chans,period,K_p,K_i,exp_FRs,volume,p_range,p_incr,max_equilibration_t,eq_duration,wpdim,wpcurrent,standard_repeats,ser)

    #--------------------------------Functions------------------------------------------
