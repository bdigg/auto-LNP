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
import flow_calculator as calc

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
    exp_FRs = [[100,100,300,None]]


#----------------------------------Controller Parameters-----------------------------------
inst_name = '01EA53FD'
active_chans = [1,2,3] #Set all active channels
#Sensor setup [Channel, Type (5-1000uL/min)(4-80uL/min) , Digital (1), Calibration (H20 -0), Pixel (7) ]
sensor1 = [1,5,1,0]#[1,4,1,0]
sensor2 = [2,5,1,0]
sensor3 = [3,4,1,0]
sensor4 = None #[4,5,1,0]
#Pressure calibrate
pressure_calibrate = "default"

#Flow rates of each input channel
volume = 100 #volume produced in micro litres

#Repeats
standard_repeats = 1 #How many tines should each composition be repeated
fail_repeats = 1 #If FR falls out of range, how many repeats 

#PI Controller Parameters
period = 0.5
K_p = [0.01,0.0005,0.001] #Tune the proportioal component 0.018
K_i = 0.0001 #Tune the integral component  0.0005
p_range = [0,80] #min,max

#Experiment timings
max_equilibration_t = 300 #Maximum time to reach FR equilibrium
eq_duration = 15 #Time over which the FR must be stable
experiment_t = 30 # 

#----------------------------------Initiation-----------------------------------
error = 0 
while error == 0:
    error = pump.pressure_init()
    error = pump.sensor_init(sensor1, sensor2, sensor3, sensor4)
    #error = pump.pressure_calib(pressure_calibrate)
    #error = pump.flush(active_chans,100,(1*60)) #pressure 
    #error = pump.stability_test(active_chans,[20,40,80,100])
    pump.flowtable(active_chans,)
    #K_p,K_i = pump.auto_tune(active_chans,period)
    #---------------------------------Main Loop------------------------------------
    main_loop = True

    if main_loop == True:
        #Run Experiments, repeating as specified 
        for i, FR in enumerate(exp_FRs):
            repeats = 0   
            while repeats < standard_repeats:
                #experiment_t = volume/exp_params[i][0]
                print("Beginning experiment: ", FR)
                collection,consistent_fr = pump.main_PI(period,K_p,K_i,FR,experiment_t,max_equilibration_t,eq_duration)
                if consistent_fr == False:
                    repeats += -1
                repeats += 1
                control = input("Continue? (y)")
        pump.stop()

    #--------------------------------Functions------------------------------------------
