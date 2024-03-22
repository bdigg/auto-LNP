import pump
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import threading
import expel


def flush(active_channels, pressure, last_t):
    print("Flushing System")
    for i, channel in enumerate(active_channels):
        start_t = time.time() 
        error = pump.set_pressure(channel,pressure)
        print("Channel",channel,"Pressure",pressure)
    while True:
        if (time.time() - start_t) > last_t:
            break
    return error

def stability_test(active_channels, pressures): #update to give live plot and value for stability
    print("Stability Test")
    for pressure in pressures:
        for channel in active_channels:
            error = pump.set_pressure(channel,pressure)
            print("Channel",channel,"Pressure",pressure)
        print("Wait 10 seconds")
        time.sleep(10)
        start_t,last_t = time.time(),time.time()
        exp_t = 5
        t = 0
        prange = [[],[],[],[]]
        while True:
            for i, channel in enumerate(active_channels):
                flowrate = pump.get_sensor_data(channel)
                print(channel,pump.get_sensor_data(channel))
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

    flow_list, cont_press_list, real_press_list = [[],[],[],[]],[[],[],[],[]],[[],[],[],[]]
    time_list = []
    start_t = time.time()
    last_t = start_t

    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)

    for ref_press in ref_pressure:
        for channel in enumerate(active_channels):
            pump.set_pressure(channel,ref_press)
        for inc_press in inc_pressure:
            for j, channel in enumerate(active_channels):
                print("Control P -",channel, inc_press)
                cont_press_list[i].append(inc_press)
                pump.set_pressure(channel,inc_press)
                sleep_t = period - (time.time() - last_t)
                if sleep_t > 0:
                    time.sleep( sleep_t )
                fr = pump.get_sensor_data(i)[0]
                flow_list[i].append(fr)
                print("Flow rate -",channel,fr)
                pr = pump.get_pressure_data(1)[0]  
                real_press_list[i].append(pr)  
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

def stop():
    pump.set_pressure(1,0)
    pump.set_pressure(2,0)
    pump.set_pressure(3,0)
    pump.set_pressure(4,0)

def auto_tune(active_chans,period):
    print("Auto Tune")
    Kp, Ki = [],[]
    for chan in active_chans:
        start_t = time.time()
        press_val = 0
        prev_output = pump.get_sensor_data(chan)

        while True:
            current_t = time.time()
            elapsed_t = current_t - start_t
        
            if elapsed_t >= 5:
                start_t = current_t
                press_val = (1 - press_val)*50
                pump.set_pressure(chan,press_val)

            output = pump.get_sensor_data()

            if (output - prev_output) * (output - 10.0) < 0:
                period = elapsed_t
                ultimate_gain = output
                break

            previous_output = output

        Kp.append(0.45 * ultimate_gain)
        Ki.append(2 * Kp / period)
                  
def main_PI(autocollect,active_channels,period,K_p,K_i,exp_FRs,volume,p_range,p_incr,eqb_t,eqb_d,wpdim,wpcurrent,standard_repeats,ser):
    #Empty arrays to save data to
    flow_list, t_list, real_press_list, cont_press_list = [[],[],[],[]],[],[[],[],[],[]],[[],[],[],[]]
    #Global PID variables
    pr_control, I = [0,0,0,0],[0,0,0,0]


    #Setup live flow figure
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    col_list,switch_list = [],[]

    real_start_t = time.time()

    #Iteration through each of the flow rates
    for i, set_FR in enumerate(exp_FRs): 
        repeats = 0   
        exp_t = (volume/np.sum(set_FR[0:(len(active_channels)-1)]))*60
        while repeats < standard_repeats: #Gives the option to repeat a given flowrate condition
            print("Beginning experiment: ", set_FR)
            fr, fr_perc_error, fr_perc_error_max, consistent_fr = [0,0,0,0],[],[],[]
            collection = False

            switch_list.append((time.time() - real_start_t))

            #Read inital time
            active_t = eqb_t
            start_t = time.time() # <- This must be close to the routine
            last_t = start_t
            t = 0

            print("Start Equilibration Stage")
            #print("Sample",x,"Flow rates:",)
            while True:
                #-----Main PID Loop-----
                t_list.append((time.time() - real_start_t))
                for i, channel  in enumerate(active_channels):
                    #Flow rate reading
                    fr[i] = pump.get_sensor_data(channel)[0]
                    if channel > 1: #If a lipid channel (in ethanol) make adjustment
                        fr[i] = (fr[i] - 80.09)*4.05
                    flow_list[i].append(fr[i])
                    fr_error = fr[i]-set_FR[i]
                    fr_perc_error.append(abs(fr_error/set_FR[i]))
                    #Pressure reading
                    pr = pump.get_pressure_data(channel)[0]  
                    real_press_list[i].append(pr)  
                    #Correction calculations
                    I[i] = I[i] + K_i*fr_error*(period)
                    adjustment =  (fr_error*abs(fr_error))*K_p[i] + I[i]
                    if adjustment > p_incr[1]: adjustment = p_incr[1]
                    if adjustment < p_incr[0]: adjustment = p_incr[0]  
                    pr_control[i] = pr_control[i] - adjustment 
                    if pr_control[i] > p_range[1]: pr_control[i] = p_range[1]
                    if pr_control[i] < p_range[0]: pr_control[i] = p_range[0]
                    cont_press_list[i].append(pr_control[i])
                    pump.set_pressure(channel,pr_control[i]) 
                    
                    fr_perc_error_max.append(np.max(fr_perc_error))
                    fr_perc_error = []

                if t > eqb_d*(int(1/period)):
                    if np.max((fr_perc_error_max)[(t-eqb_d*(int(1/period))):t]) < 0.075 and collection == False:
                        print(np.max((fr_perc_error_max)[(t-eqb_d*2):t]))
                        print("Beginning Collection\n\n\n")
                        #Move to well position
                        if autocollect == True:
                            threading.Thread(target=expel.wastetowell,args=(ser, wpcurrent)).start()
                        collection = True
                        start_t = time.time()
                        col_list.append((time.time() - real_start_t))
                        active_t = exp_t
                    elif np.max((fr_perc_error_max)[(t-eqb_d*(int(1/period))):t]) > 0.1 and collection == True:
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
                chancolours = ["lightseagreen","darkorange","darkred","blueviolet"]
                for i, chan in enumerate(active_channels):
                    ax1.plot(t_list,flow_list[i],label="Channel %d" % chan, color=chancolours[i])
                    ax2.plot(t_list,cont_press_list[i],label="Channel %d" % chan,color=chancolours[i])
                    ax1.axhline(y=set_FR[i],color=chancolours[i],linewidth=0.5, alpha=0.5)
                for timex in switch_list:
                    ax1.axvline(x=timex,color='r',linestyle='--')
                    ax2.axvline(x=timex,color='r',linestyle='--')
                for timex in col_list:
                    ax1.axvline(x=timex,color='k',linestyle=':')
                    ax2.axvline(x=timex,color='k',linestyle=':')                    
                ax1.set_ylim(0, np.amax(exp_FRs)*1.1)
                ax2.set_ylim(0,p_range[1])
                ax1.legend()
                ax2.legend()
                plt.title('Flow')
                ax1.set_ylabel('flow [uL/min]')
                ax2.set_ylabel('pressure [mbar]')
                plt.xlabel('Time (s)')
                plt.pause(0.0001)
                plt.show(block=False)

            if autocollect == True:  
                threading.Thread(target=expel.currenttowaste,args=(ser, wpcurrent)).start()

            for i, chan in enumerate(active_channels):
                print(i,t,exp_t)
                consistent_fr.append(np.max((fr_perc_error_max)[(t-int(exp_t)*(int(1/period))):t]))
                    
            if collection == False:
                print("Equilibration Failed - error", consistent_fr)
            else:
                print("Collection Successful - error", consistent_fr) 

            if consistent_fr == False:
                repeats += -1
            repeats += 1
            #save wp positions with exp info
            if autocollect == True:
                wpprev = wpcurrent
                if wpcurrent[1] == wpdim[1]:
                    wpcurrent[1] = 1
                    wpcurrent[0] = wpcurrent[0] + 1
                else:
                    wpcurrent[1] = wpcurrent[1] + 1
                print("Current plate position: ",wpcurrent)
    stop()    
    return()
    
