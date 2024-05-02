#Install packages for pressure devices
import sys
from email.header import UTF8
sys.path.append('./DLL64')
sys.path.append('./Elveflow64.py')
from ctypes import *
from array import array
from Elveflow64 import *
Instr_ID = c_int32()
import numpy as np
import ctypes as ct


# Input the setup type
def pressure_init():
    print("Instrument name and regulator types are hardcoded in the Python script")
    #Insert Machine Code HERE
    error = OB1_Initialization('0204B3ED'.encode('ascii'),2,2,2,2,byref(Instr_ID)) 
    print('error:%d' % error)
    print("OB1 ID: %d" % Instr_ID.value)
    return error

def sensor_init(sensor1, sensor2, sensor3, sensor4):
    if sensor1 != None:
        error1=OB1_Add_Sens(Instr_ID, sensor1[0], sensor1[1], sensor1[2], sensor1[3], 7, 0)
    if sensor2 != None:
        error2=OB1_Add_Sens(Instr_ID, sensor2[0], sensor2[1], sensor2[2], sensor2[3], 7, 0)
    if sensor3 != None:
        error3=OB1_Add_Sens(Instr_ID, sensor3[0], sensor3[1], sensor3[2], sensor3[3], 7, 0)
    if sensor4 != None:
        error4=OB1_Add_Sens(Instr_ID, sensor4[0], sensor4[1], sensor4[2], sensor4[3], 7, 0)

    print('error add digit flow sensor:',error1,error2,error3,error4)
    return error1

Calib = (c_double*1000)()
def pressure_calib(answer):
    print("Pressure calib")
    while True:
        if answer == 'default':
            error = Elveflow_Calibration_Default (byref(Calib),1000)
            calibarr = byref(Calib)
            print("Default Calibration taken")
            break
        if answer == 'load':
            #error = Elveflow_Calibration_Load (Calib_path.encode('ascii'), byref(Calib), 1000)
            array = np.load("C:/Users/bdigg/OneDrive/Documents/GitHub/auto-LNP/auto-LNP/calib.npy")
            array.ctypes.data
            calibarr = array.ctypes.data_as(ct.POINTER(ct.c_double*1000))
            error = 0
            break
        if answer == 'new':
            OB1_Calib (Instr_ID.value, Calib, 1000)
            np.save("C:/Users/bdigg/OneDrive/Documents/GitHub/auto-LNP/auto-LNP/calib",Calib)
            print('Calib saved in calib.npy')
            break
    return calibarr,error

def set_pressure(set_channel,set_pressure,calibarr):
    set_channel=int(set_channel) # convert to int
    set_channel=c_int32(set_channel) # convert to c_int32
    set_pressure=float(set_pressure) 
    set_pressure=c_double(set_pressure) # convert to c_double
    error=OB1_Set_Press(Instr_ID.value, set_channel, set_pressure, calibarr ,1000) 
    return error 

def get_sensor_data(sensor_channel):
    data_sens=c_double()
    set_channel=int(sensor_channel) # convert to int
    set_channel=c_int32(sensor_channel) # convert to c_int32
    error=OB1_Get_Sens_Data(Instr_ID.value,set_channel, 1,byref(data_sens)) # Acquire_data=1 -> read all the analog values
    return data_sens.value, error

def get_pressure_data(press_channel,calibarr):
    set_channel=c_int32( int(press_channel) ) # convert to c_int32
    get_pressure=c_double()
    error=OB1_Get_Press(Instr_ID.value, set_channel, 1, calibarr ,byref(get_pressure), 1000) # Acquire_data=1 -> read all the analog values  #byref(Calib)
    return get_pressure.value, error
