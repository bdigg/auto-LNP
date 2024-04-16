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

    #load compositions from doc  

    expname = "DPPCLSCHOL"

    #Channel 1 - Buffer 
    Buffer = ["Buffer_Name",True, range(180,180+1,20)]

    #Channel 2 - Lipid 1 in ethanol
    #Lp1=[Name, MW, Range , Concentration]  
    Lp1 = ["DPPC", 100, "Base",  10]  

    #Channel 3 - Lipid 2 in ethanol - if not active, set range to 0
    #Lp2= [Name, MW, Range , Concentration]  
    Lp2 = ["LysoPC", 50, range(0,(10+1),5), 5]  

    #Channel 4 - Lipid 3 in ethanol - if not active, set range to 0
    #Lp3= [Name, MW, Range , Concentration]  
    Lp3 = ["Chol", 50, range(0,(10+1),5), 5]   

    exp_params,exp_FRs = calc.flow_calc(FRR_range,Buffer,Lp1,Lp2,Lp3)
    print(exp_FRs)

elif Mode == "Flow":
    expname = "FlowTest150424"
    exp_FRs = [[50,50,50,50],[40,40,40,40],[60,60,60,60],[70,70,70,70],[80,80,80,80],[30,30,30,30]]
    exp_params = calc.genparams(exp_FRs)

#----------------------------------Controller Parameters-----------------------------------
inst_name = '01EA53FD'
active_chans = [1,2,3,4] #Set all active channels
#Sensor setup [Channel, Type (5-1000uL/min)(4-80uL/min) , Digital (1), Calibration (H20 -0), Pixel (7) ]
sensor1 = [1,5,1,0]#[1,4,1,0]
sensor2 = [2,5,1,0]  ##IMPORTANT Change calibration if using MFS3 sensor - control.py PID
sensor3 = [3,5,1,0]
sensor4 = [4,5,1,0]
#Pressure calibrate
pressure_calibrate = "default"

#Flow rates of each input channel#
volume = 50 #volume produced in micro litres

#Repeats
standard_repeats = 1 #How many tines should each composition be repeated
fail_repeats = 1 #If FR falls out of range, how many repeats 

#PI Controller Parameters
period = 0.2
K_p = [0.02,0.01,0.01,0.01] #Tune the proportional component 0.018 [0.04,0.01,0.01,0.01]
K_i = 0.00001 #Tune the integral component  0.0005
p_incr = [-50,50] #min,max
p_range = [0,400] #min,max

#Experiment timings
max_equilibration_t = 120 #Maximum time to reach FR equilibrium
eq_duration = 5 #Time over which the FR must be stable

#Autocollect Configuration 
autocollect = True
wpdim = [8,12] #row col
wpcurrent = [1,1] #set this as the first well to be used

tubingdim = [0.51,30] #Tubing internal diam in mm, length after chip in cm
#add wp dimensions in mm etc for conversion
#----------------------------------Initiation-----------------------------------
global ser
ser = 0
if autocollect  == True:
    ser = expel.serconnect()
    #expel.homeandfirst(ser)
error = pump.pressure_init()
error = pump.sensor_init(sensor1, sensor2, sensor3, sensor4)
error = control.flush(active_chans,80,(0.1*60)) #pressure 
#error = control.stability_test(active_chans,[20,40,80,100])
#control.flowtable(active_chans,)
#K_p,K_i = control.auto_tune(active_chans,period)
    #---------------------------------Main Loop------------------------------------
main_loop = True
if main_loop == True:
    control.main_PI(expname,exp_params,autocollect,active_chans,period,K_p,K_i,exp_FRs,volume,p_range,p_incr,max_equilibration_t,eq_duration,wpdim,wpcurrent,tubingdim,standard_repeats,ser)
    #--------------------------------Functions------------------------------------------
