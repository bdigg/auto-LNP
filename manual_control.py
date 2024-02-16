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
#Sensor setup [Channel, Type (5-1000uL/min), Digital (1), Calibration (H20 -0), Pixel (7) ]
sensor1 = [1,5,1,0]
sensor2 = None #[2,5,1,0]
sensor3 = None #[3,5,1,0]
sensor4 = None #[4,5,1,0]
#Pressure calibrate
pressure_calibrate = "default"

FR = [50,None,None,None]

#----------------------------------Initiation-----------------------------------
pump.pressure_init()
pump.sensor_init(sensor1, sensor2, sensor3, sensor4)
pump.pressure_calib(pressure_calibrate)
#---------------------------------Main Loop------------------------------------
K_p = 0.01
p_range = [0,100] #min,max

experiment_t = 60

pump.main_PID(K_p,FR,experiment_t)

#Set limits for flow control - once x flow reached, begin exp for x seconds