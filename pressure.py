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
import matplotlib.animation as animation
import numpy as np
#import control.matlab as mlcontrol

Instr_ID = c_int32()

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
        error=OB1_Add_Sens(Instr_ID, sensor1[0], sensor1[1], sensor1[2], sensor1[3], 7, 0)
    if sensor2 != None:
        error=OB1_Add_Sens(Instr_ID, sensor2[0], sensor2[1], sensor2[2], sensor2[3], 7, 0)
    if sensor3 != None:
        error=OB1_Add_Sens(Instr_ID, sensor3[0], sensor3[1], sensor3[2], sensor3[3], 7, 0)
    if sensor4 != None:
        error=OB1_Add_Sens(Instr_ID, sensor4[0], sensor4[1], sensor4[2], sensor4[3], 7, 0)

    print('error add digit flow sensor:%d' % error)
    return error

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
    return error

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

def flush(active_channels, pressure, last_t):
    print("Flushing System")
    for i, channel in enumerate(active_channels):
        error = set_pressure(channel,pressure)

    start_t = time.time() 
    exp_t = last_t
    while True:
        if (time.time() - start_t) > exp_t:
            break
    return error

def stability_test(active_channels, pressures):
    print("Stability Test")
    for pressure in pressures:
        for channel in active_channels:
            error = set_pressure(channel,pressure)
            print("Channel",channel,"Pressure",pressure)
        print("Wait 10 seconds")
        time.sleep(10)
        start_t,last_t = time.time(),time.time()
        exp_t = 5
        t = 0
        prange = [[],[],[],[]]
        while True:
            for i, channel in enumerate(active_channels):
                flowrate = get_sensor_data(channel)
                print(channel,get_sensor_data(channel))
            print(t,"seconds")
            if (time.time() - start_t) > exp_t:
                break
            # Wait until desired period time
            sleep_t = 1 - (time.time() - last_t)
            if sleep_t > 0:
                time.sleep( sleep_t )
            last_t = time.time() # And update the last time  
            t += 1   
    return error      

def flowtable(active_channels,):
    experiment_t = 3
    period = 5
    start_t = time.time()
    last_t = start_t
    ref_pressure = [0,10,20,30,40,50,60,70,80,90,100]
    inc_pressure = [0,10,20,30,40,50,60,70,80,90,100]

    flow_list, cont_pressure_list, real_pressure_list = [[],[],[],[]],[[],[],[],[]],[[],[],[],[]]
    start_t = time.time()
    last_t = start_t

    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)

    for ref_press in ref_pressure:
        for channel in enumerate(active_channels):
            set_pressure(channel,ref_press)
        for inc_press in inc_pressure:
            for j, channel in enumerate(active_channels):
                print("Control P -",channel, inc_press)
                cont_pressure_list[i].append(inc_press)
                set_pressure(channel,inc_press)
                sleep_t = period - (time.time() - last_t)
                if sleep_t > 0:
                    time.sleep( sleep_t )
                fr = get_sensor_data(i)[0]
                flow_list[i].append(fr)
                print("Flow rate -",channel,fr)
                pr = get_pressure_data(1)[0]  
                real_pressure_list[i].append(pr)  
                print("Actual P -", pr,"\n----")
                
                last_t = time.time() # And update the last time
        
                ax1.clear()
                ax2.clear()
                for i, chan in enumerate(active_channels):
                    ax1.plot(time_list,flow_list[i],label="Channel %d" % chan)
                    ax2.plot(time_list,cont_press_list[i],label="Channel %d" % chan)
                ax1.legend()
                ax2.legend()
                plt.title('Flow')
                ax1.set_ylabel('flow [uL/min]')
                ax2.set_ylabel('pressure [mbar]')
                plt.xlabel('Time (s)')
                plt.pause(0.0001)
                plt.show(block=False)

def auto_tune(active_chans,period):
    print("Auto Tune")
    Kp, Ki = [],[]
    for chan in active_chans:
        start_t = time.time()
        press_val = 0
        prev_output = get_sensor_data(chan)

        while True:
            current_t = time.time()
            elapsed_t = current_t - start_t
        
            if elapsed_t >= 5:
                start_t = current_t
                press_val = (1 - press_val)*50
                set_pressure(chan,press_val)

            output = get_sensor_data()

            if (output - prev_output) * (output - 10.0) < 0:
                period = elapsed_t
                ultimate_gain = output
                break

            previous_output = output

        Kp.append(0.45 * ultimate_gain)
        Ki.append(2 * Kp / period)
        
        


def main_PI(period,K_p,K_i,set_FR,exp_t,eqb_t,eqb_d):

    active_channels, fr, fr_perc_error, pr_control = [],[0,0,0,0],[[],[],[],[]],[0,0,0,0]
    collection = False

    #Set the inital pressure and get first pressure reading
    for n, FR in enumerate(set_FR):
        if FR != None:
            active_channels.append(n+1)
            set_pressure(n+1,5) 


    # Set the reference
    flow_list, time_list, real_press_list, cont_press_list = [[],[],[],[]],[],[[],[],[],[]],[[],[],[],[]]
    meas_flow = [c_double(), c_double(), c_double(), c_double()]
    control_val = [c_double(), c_double(), c_double(), c_double()]

    #Read inital time
    active_t = eqb_t
    start_t = time.time() # <- This must be close to the routine
    last_t = start_t
    real_start_t = start_t
    t = 0
    I,consistent_fr = [0,0,0,0],[]
    
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
  

    print("Start Equilibration Stage")
    #print("Sample",x,"Flow rates:",)
    while True:
        time_list.append((time.time() - real_start_t))
        for i, channel  in enumerate(active_channels):
            fr[i] = get_sensor_data(channel)[0]
            if channel > 1: #If a lipid channel (in ethanol) make adjustment
                fr[i] = (fr[i] - 4.52)*6.9
            flow_list[i].append(fr[i])
            fr_error = fr[i]-set_FR[i]
            fr_perc_error[i].append(abs(fr_error/set_FR[i]))
            pr = get_pressure_data(channel)[0]  
            real_press_list[i].append(pr)  
            I[i] = I[i] + K_i*fr_error*(period)
            adjustment =  (fr_error*abs(fr_error))*K_p[i] + I[i]
            if adjustment > 20:
                adjustment = 20
            if adjustment < -20:
                adjustment = -20  
            pr_control[i] = pr_control[i] - adjustment 
            if pr_control[i] > 100:
                pr_control[i] = 100
            if pr_control[i] < 0:
                pr_control[i] = 0
            cont_press_list[i].append(pr_control[i])
            set_pressure(channel,pr_control[i]) 
        print("Ch1-FR {:.2f}".format(fr[0]),"Ch2-FR {:.2f}".format(fr[1]),"Ch3-FR {:.2f}".format(fr[2]))

        if t > eqb_d*2:
            if np.max((fr_perc_error[i])[(t-eqb_d*2):t]) < 0.05 and collection == False:
                print(np.max((fr_perc_error[i])[(t-eqb_d*2):t]))
                print("Beginning Collection\n\n\n")
                #Move to well position
                collection = True
                start_t = time.time()
                collect_t = time.time()
                active_t = exp_t
            elif np.max((fr_perc_error[i])[(t-eqb_d*2):t]) > 0.1 and collection == True:
                print("Flow rate condition fail")
    

        if (time.time() - start_t) > active_t:
            break

        # Wait until desired period time
        sleep_t = period - (time.time() - last_t)
        if sleep_t > 0:
            time.sleep( sleep_t )
        last_t = time.time() # And update the last time 
        t = t+1
        
        ax1.clear()
        ax2.clear()
        for i, chan in enumerate(active_channels):
            ax1.plot(time_list,flow_list[i],label="Channel %d" % chan)
            ax2.plot(time_list,cont_press_list[i],label="Channel %d" % chan)
        #if collection == True:
        #    ax1.plot([collect_t,collect_t],np.linspace(np.min(cont_press_list),np.max(cont_press_list),2),'r')
        #    ax2.plot([collect_t,collect_t],np.linspace(np.min(cont_press_list),np.max(cont_press_list),2),'r')
        ax1.legend()
        ax2.legend()
        plt.title('Flow')
        ax1.set_ylabel('flow [uL/min]')
        ax2.set_ylabel('pressure [mbar]')
        plt.xlabel('Time (s)')
        plt.pause(0.0001)
        plt.show(block=False)


    for i, chan in enumerate(active_channels):
        consistent_fr.append(np.max((fr_perc_error[i])[(t-exp_t*2):t]))
    
    if collection == False:
        print("Equilibration Failed - error", consistent_fr)
    else:
        print("Collection Successful - error", consistent_fr) 

    return(collection,consistent_fr)

def stop():
    set_pressure(1,0)
    set_pressure(2,0)
    set_pressure(3,0)
    set_pressure(4,0)