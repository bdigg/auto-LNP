#import sys
#import pandas as pd
#from email.header import UTF8
#sys.path.append('./DLL64')
#sys.path.append('./Elveflow64.py')
#from ctypes import *
#from array import array
#from Elveflow64 import *
#import time
import numpy as np
#import matplotlib.pyplot as plt
import pump 
import control
import flow_calculator as calc
import expel
import records
import threading
#Instr_ID = c_int32()

#----------------------------------Record Keeping------------------------------------------
id = records.id()
Date = "240513"#records.date() #YMD
ExpTitle = "AutoCalib"
Details = "Calibration Curve on Channels 1 and 2 "

BufferName = "MilliQ"
BufferDetails = "From the stock in the lipid lab"
Lp1Name = "NBD-PE"
Lp1Notes = "NBDPE 1:16. 0.05mg/ml. Made 6ml with 300ul of 1mg/ml NBDPE in choloraform"
Lp2Name = "Ethanol"
Lp2Notes = "99.5% Pure - MHF Stock"
Lp3Name = "Ethanol"
Lp3Notes = "99.5% Pure - MHF Stock"

expname = "2-240513-AutoCalib-part2"

#----------------------------------Experiment Parameters-----------------------------------
#Mode = "Composition"
Mode = "FlowControl"

if Mode == "Composition":
    #FRR
    FRR_range = range(1,10+1,1) #[min,max,increment]

    #load compositions from doc  

    #Channel 1 - Buffer 
    Buffer = ["Buffer_Name",True, range(60,60+1,20)]

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

elif Mode == "FlowControl":
    exp_FRs = [[40,40,0.001,0.001],[30,45,0.001,0.001],[20,46.66,0.001,0.001],[10,40,0.001,0.001],[5,45,0.001,0.001],[-2,60,0.001,0.001]]
    # [40,40,0.001,0.001],[30,45,0.001,0.001],[20,46.66,0.001,0.001],[10,40,0.001,0.001],[5,45,0.001,0.001],[0.001,60,0.001,0.001]
    #[[0.001,60,0.001,0.001],[2.222,60,2.222,2.222],[5,60,5,5],[8.57,60,8.57,8.57],[13.33,60,13.33,13.33],[20,60,20,20],[30,60,30,30],[46.66,60,46.66,46.66],[40,30,40,40],[60,20,60,60],[20,0.001,20,20]]
    exp_params = calc.genparams(exp_FRs)

elif Mode == "Pressure Control":
    print("Preesss")

elif Mode == "Manual Control":
    print("Manuall")

#----------------------------------Controller Parameters-----------------------------------
inst_name = '01EA53FD'
active_chans = [1,2,3,4] #Set all active channels  [1,2,3,4] 
#Sensor setup [Channel, Type (5-1000uL/min)(4-80uL/min) , Digital (1), Calibration (H20 -0), Pixel (7) ]
sensor1 = [1,5,1,0]#[1,4,1,0]
sensor2 = [2,5,1,0]  ##IMPORTANT Change calibration if using MFS3 sensor - control.py PID
sensor3 = [3,5,1,0]
sensor4 = [4,5,1,0]
sensorcorr = [[1.1183,-6.4631],[1.8076,-7.9951],[1.7487,-9.2466],[1.9081,-7.7105]] #Sensor calibration corrections

#Flow rates of each input channel#
volume = 60 #volume produced in micro litres

#Repeats
standard_repeats = 3  #How many tines should each composition be repeated
fail_repeats = 1 #If FR falls out of range, how many repeats 

#PI Controller Parameters
period = 0.2
K_p = np.array([200,30,30,30]) #Tune the proportional component 0.018 [0.02,0.01,0.01,0.01]#[0.04,0.008,0.008,0.008]65um[200,30,30,30]
K_i = 0.0001 #Tune the integral component  0.0005 65um 0.0001
p_incr = [-500,500] #min,max 65um [-500,500]
p_range = [0,2000] #min,max 65um [0,2000]


#Experiment timings
max_equilibration_t = 120 #Maximum time to reach FR equilibrium
eq_duration = 15  #Time over which the FR must be stable - Must be at least time to go through outlet tubing!!!

#Equilibrium Conditions
Eqpercerror = 5
Expelpercerror = 10

#Autocollect Configuration 
autocollect = True
autohome = False #Set to False if autocollecting but dont need to rehome - i.e already over the first well
wpdim = [8,12] #row col
wpcurrent = [7,1] #set this as the first well to be used

#----------------------------------Initiation-----------------------------------
ser = expel.initialise(autocollect,autohome,wpcurrent)
pump.pressure_init()
calibarr,error = pump.pressure_calib("load")
pump.sensor_init(sensor1, sensor2, sensor3, sensor4)
#error = control.flush(active_chans,100,(0.1*60),calibarr) #pressure 
    #---------------------------------Main Loop------------------------------------
main_loop = True
if main_loop == True:
    control.main_PI(expname,exp_params,autocollect,active_chans,sensorcorr,period,K_p,K_i,exp_FRs,volume,p_range,p_incr,max_equilibration_t,eq_duration,wpdim,wpcurrent,standard_repeats,ser,calibarr)
    #--------------------------------Functions------------------------------------------
