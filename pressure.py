#Install packages for pressure devices
import sys
from email.header import UTF8
sys.path.append('./DLL64')
sys.path.append('./Elveflow64.py')
from ctypes import *
from array import array
from Elveflow64 import *
import time
import matplotlib.pyplot as plt
import numpy as np

Instr_ID = c_int32()

# Input the setup type
def pressure_init():
    print("Instrument name and regulator types are hardcoded in the Python script")
    #Insert Machine Code HERE
    error = OB1_Initialization('01EA53FD'.encode('ascii'),2,2,2,2,byref(Instr_ID)) 
    print('error:%d' % error)
    print("OB1 ID: %d" % Instr_ID.value)

def sensor_init(sensor1, sensor2, sensor3, sensor4):
    if sensor1 != None:
        error=OB1_Add_Sens(Instr_ID, sensor1[0], sensor1[0], sensor1[0], sensor1[0], 7, 0)
    if sensor2 != None:
        error=OB1_Add_Sens(Instr_ID, 2, 10, 0, 0, 7, 0)
    if sensor3 != None:
        error=OB1_Add_Sens(Instr_ID, 3, 10, 0, 0, 7, 0)
    if sensor4 != None:
        error=OB1_Add_Sens(Instr_ID, 3, 10, 0, 0, 7, 0)

    print('error add digit flow sensor:%d' % error)

Calib = (c_double*1000)()
def pressure_calib(answer):
    print("Pressure calib")
    while True:
        Calib_path = './Calib.txt'
        if answer == 'default':
            error = Elveflow_Calibration_Default (byref(Calib),1000)
            print("Default Calibration taken")
            break
        if answer == 'load':
            error = Elveflow_Calibration_Load (Calib_path.encode('ascii'), byref(Calib), 1000)
            break
            
        if answer == 'new':
            OB1_Calib (Instr_ID.value, Calib, 1000)
            error = Elveflow_Calibration_Save(Calib_path.encode('ascii'), byref(Calib), 1000)
            print('Calib saved in %s' % Calib_path.encode('ascii'))
            break

def set_pressure(set_channel,set_pressure):
    set_channel=int(set_channel) # convert to int
    set_channel=c_int32(set_channel) # convert to c_int32
    set_pressure=float(set_pressure) 
    set_pressure=c_double(set_pressure) # convert to c_double
    error=OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, byref(Calib),1000) 
    return error 

def get_sensor_data(sensor_channel):
    data_sens=c_double()
    set_channel=int(sensor_channel) # convert to int
    set_channel=c_int32(sensor_channel) # convert to c_int32
    error=OB1_Get_Sens_Data(Instr_ID.value,set_channel, 1,byref(data_sens)) # Acquire_data=1 -> read all the analog values
    return data_sens.value, error

def get_pressure_data(press_channel):
    set_channel=c_int32( int(press_channel) ) # convert to c_int32
    get_pressure=c_double()
    error=OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib),byref(get_pressure), 1000) # Acquire_data=1 -> read all the analog values
    return get_pressure.value, error

# Controller parameters: Very soft controller

# OB1 arrangement
period = 0.5

def main_PI(K_p,K_i,set_FR,exp_t,eqb_t):

    active_channels, fr, fr_perc_error, fr_perc_error_prev, pr_control = [],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]
    collection = False

    #Set the inital pressure and get first pressure reading
    for n, FR in enumerate(set_FR):
        if FR != None:
            set_pressure(n+1,5)
            active_channels.append(n+1)
            pr_control[n] = get_pressure_data(n+1)[0]

    # Set the reference
    flow_list = [[],[],[],[]]
    control_list = [[],[],[],[]]
    meas_flow = [c_double(), c_double(), c_double(), c_double()]
    control_val = [c_double(), c_double(), c_double(), c_double()]

    #Read inital time
    active_t = eqb_t
    start_t = time.time() # <- This must be close to the routine
    last_t = start_t
    I = 0

    print("Start Equilibration Stage")
    #print("Sample",x,"Flow rates:",)
    while True:
        for i, channel  in enumerate(active_channels):
            fr[i] = get_sensor_data(channel)[0]
            #flow_list.append(fr)
            print("Flow rate Channel",channel,"-",fr[i])
            fr_error = fr[i]-set_FR[i]
            fr_perc_error[i] = fr_error/set_FR[i]
            pr = get_pressure_data(channel)[0]  
            #real_pressure_list.append(pr)  
            I = I + K_i*fr_error*(period)
            adjustment =  fr_error*K_p + I
            pr_control[i] = pr_control[i] - adjustment 
            #cont_pressure_list.append(pr_control)
            set_pressure(channel,pr_control[i])
    
        if np.max(fr_perc_error,fr_perc_error_prev) < 0.05 and collection == False:
            print("Beginning Collection")
            #Move to well position
            collection = True
            eqb_t =  time.time() + exp_t + start_t
        elif np.max(fr_perc_error,fr_perc_error_prev) > 0.05 and collection == True:
            print("Flow rate condition fail")
            consistent_fr = False
        fr_perc_error_prev = fr_perc_error

        if (time.time() - start_t) > active_t:
            break
        # Wait until desired period time
        sleep_t = period - (time.time() - last_t)
        if sleep_t > 0:
            time.sleep( sleep_t )
        last_t = time.time() # And update the last time 

    for i in active_channels:
        set_pressure(i,0)
    if collection == False:
        print("Equilibration Failed")


    return(collection,consistent_fr)