#Install packages for pressure devices
import sys
from email.header import UTF8
sys.path.append('./DLL64')
sys.path.append('./Elveflow64.py')
from ctypes import *
from array import array
from Elveflow64 import *
import time
import matplotlib as plt

Instr_ID = c_int64()

#Input the setup type
def pressure_init():
    print("Instrument name and regulator types are hardcoded in the Python script")
    #Insert Machine Code HERE
    error = OB1_Initialization('COM1'.encode('ascii'),2,3,4,4,byref(Instr_ID)) 
    print('error:%d' % error)
    print("OB1 ID: %d" % Instr_ID.value)

def sensor_init():
    error=OB1_Add_Sens(Instr_ID, 1, 10, 0, 0, 7, 0)
    print('error add digit flow sensor:%d' % error)

def pressure_calib(answer):
    Calib = (c_double*1000)() # Always define array this way, calibration should have 1000 elements
    while True:
        Calib_path = 'C:\\Users\\Public\\Desktop\\Calibration\\Calib.txt'
        if answer == 'default':
            error = Elveflow_Calibration_Default (byref(Calib),1000)
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
    Calib = (c_double*1000)()
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
    Calib = (c_double*1000)()
    set_channel=c_int32( int(press_channel) ) # convert to c_int32
    get_pressure=c_double()
    error=OB1_Get_Press(Instr_ID.value, set_channel, 1, byref(Calib),byref(get_pressure), 1000) # Acquire_data=1 -> read all the analog values
    return get_pressure.value, error
#Input cell 

#Run simple pressure

period = 0.1 # 10Hz
p_error = 0
i_error = 0
meas_flow = c_double()

def pid_run():
    global p_error
    global i_error
    Calib = (c_double*1000)()
    start_t = time.time() # <- This must be close to the routine
    last_t = start_t
    # Main routine
    while True:
        # Get the current output
        error=OB1_Get_Sens_Data(Instr_ID.value, fs_channel, 1, byref(meas_flow))
        flow_list.append(meas_flow.value)

        # Calculate the mathematical error
        p_error = ref_flow - meas_flow.value
        i_error += p_error
        # PI Controller equations
        P_val = K_p * p_error
        I_val = K_i * i_error
        # Anti-windup
        I_val = max(I_min, min(I_max, I_val))
        # Final control action
        p_control = P_val + I_val
        p_control = max(p_min, min(p_max, p_control)) # Safety saturation

        error_list.append(p_error)
        control_list.append(p_control)

        p_control=c_double( float(p_control) ) # Convert to c_double
        error=OB1_Set_Press(Instr_ID.value, p_channel, p_control, byref(Calib), 1000) # Return error message

        # Check if the elapsed time match the time limit
        if (time.time() - start_t) > experiment_t:
            break
        # Wait until desired period time
        sleep_t = period - (time.time() - last_t)
        if sleep_t > 0:
            time.sleep( sleep_t )
        last_t = time.time() # And update the last time

    # Turn off the pressure
    p_control = 0.0
    error=OB1_Set_Press(Instr_ID.value, p_channel, p_control, byref(Calib), 1000) # Return error message

    
def plot():
    # Plot the signals
    plt.rcParams['axes.grid'] = True
    fig=plt.figure()
    fig.suptitle("Microfluidic Circuit Control at {0:.2f}Hz".format(1/period))

    plt.subplot(2,1,1)
    plt.plot( flow_list )
    plt.ylabel('flow [uL/min]')
    plt.subplot(2,1,2)
    plt.plot( control_list )
    plt.ylabel('pressure [mbar]')

    
def run():
    pid_run()
    plot()

# Controller parameters: Very soft controller
K_p = 0.05 # <- Change this value to tune the controller
K_i = 0.1 # <- Change this value too to tune the controller
ref_flow = 60 # uL/min

p_min = 0 # <- This is only negative if you have some vacuum source
p_max = 100 # <- This depends on the Z regulator of each channel

# OB1 arrangement
p_channel = 2 # <- Change this to
fs_channel = 2 # <- your real configuration

experiment_t = 10.0 # Seconds
flow_list = []
error_list = []
control_list = []

#run()

pressure_init()
sensor_init()
pressure_calib("new")
set_pressure(1, 50)
get_sensor_data(1)
get_pressure_data(1)