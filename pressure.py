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
period = 0.1

def main_PID(K_p,K_i,FR1,FR2,FR3,FR4,exp_t):

    print("Starting main PID")
    # Start running the PI Control on remote mode
    error = OB1_Start_Remote_Measurement(Instr_ID.value, byref(Calib), 1000)
    # Start the PID Controller onsite
    if FR1 != None:
        p_channel = c_int32( int(1) ) # convert to c_int32
        fs_channel = c_int32( int(1) ) # convert to c_int32
        error = PID_Add_Remote(Instr_ID.value, p_channel, Instr_ID.value, fs_channel, K_p, K_i, 1) 
        ref_flow = c_double( float(FR1) )
        error = OB1_Set_Remote_Target(Instr_ID.value, p_channel, ref_flow)
    if FR2 != None:
        p_channel = c_int32( int(2) ) # convert to c_int32
        fs_channel = c_int32( int(2) ) # convert to c_int32
        error = PID_Add_Remote(Instr_ID.value, p_channel, Instr_ID.value, fs_channel, K_p, K_i, 1) 
        ref_flow = c_double( float(FR2) )
        error = OB1_Set_Remote_Target(Instr_ID.value, p_channel, ref_flow)
    if FR3 != None:
        p_channel = c_int32( int(3) ) # convert to c_int32
        fs_channel = c_int32( int(3) ) # convert to c_int32
        error = PID_Add_Remote(Instr_ID.value, p_channel, Instr_ID.value, fs_channel, K_p, K_i, 1) 
        ref_flow = c_double( float(FR3) )
        error = OB1_Set_Remote_Target(Instr_ID.value, p_channel, ref_flow)
    if FR4 != None:
        p_channel = c_int32( int(4) ) # convert to c_int32
        fs_channel = c_int32( int(4) ) # convert to c_int32
        error = PID_Add_Remote(Instr_ID.value, p_channel, Instr_ID.value, fs_channel, K_p, K_i, 1)
        ref_flow = c_double( float(FR4) )
        error = OB1_Set_Remote_Target(Instr_ID.value, p_channel, ref_flow)

    # Set the reference
    flow_list_ch1, flow_list_ch2, flow_list_ch3, flow_list_ch4 = [],[],[],[]
    control_list_ch1, control_list_ch2, control_list_ch3, control_list_ch4 = [],[],[],[]
    meas_flow_ch1, meas_flow_ch2, meas_flow_ch3, meas_flow_ch4  = c_double(), c_double(), c_double(), c_double()
    control_val_ch1, control_val_ch2, control_val_ch3, control_val_ch4 = c_double(), c_double(), c_double(), c_double()

    start_t = time.time() # <- This must be close to the routine
    last_t = start_t
    while True:
        if FR1 != None:
            error = OB1_Get_Remote_Data(Instr_ID.value, fs_channel, byref(control_val_ch1), byref(meas_flow_ch1))
            flow_list_ch1.append( meas_flow_ch1.value )
            control_list_ch1.append( control_val_ch1.value )
        if FR2 != None:
            error = OB1_Get_Remote_Data(Instr_ID.value, fs_channel, byref(control_val_ch2), byref(meas_flow_ch1))
            flow_list_ch1.append( meas_flow_ch1.value )
            control_list_ch1.append( control_val_ch1.value )
        if FR3 != None: 
            error = OB1_Get_Remote_Data(Instr_ID.value, fs_channel, byref(control_val_ch3), byref(meas_flow_ch1))
            flow_list_ch1.append( meas_flow_ch1.value )
            control_list_ch1.append( control_val_ch1.value )
        if FR4 != None:
            error = OB1_Get_Remote_Data(Instr_ID.value, fs_channel, byref(control_val_ch4), byref(meas_flow_ch1))
            flow_list_ch1.append( meas_flow_ch1.value )
            control_list_ch1.append( control_val_ch1.value )

        # Check if the elapsed time match the time limit
        if (time.time() - start_t) > exp_t:
            break
        # Wait until desired period time
        sleep_t = period - (time.time() - last_t)
        if sleep_t > 0:
            time.sleep( sleep_t )
        last_t = time.time() # And update the last time

    error = OB1_Stop_Remote_Measurement(Instr_ID.value)
    print('Stop. Error value: %d' % error)

    # Plot the signals
    plt.rcParams['axes.grid'] = True
    fig=plt.figure()
    fig.suptitle("Remote PID Control")

    plt.subplot(2,1,1)
    plt.plot(flow_list_ch1)
    plt.ylabel('flow [uL/min]')
    plt.subplot(2,1,2)
    plt.plot(control_list_ch1)
    plt.ylabel('pressure [mbar]')