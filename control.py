import pump
import time
import matplotlib.pyplot as plt
import numpy as np
import threading
import expel
import threading
import flow_calculator as calc
import records


def flush(active_channels, pressure, last_t,calibarr):
    print("Flushing System")
    for i, channel in enumerate(active_channels):
        start_t = time.time() 
        error = pump.set_pressure(channel,pressure,calibarr)
        print("Channel",channel,"Pressure",pressure)
    while True:
        if (time.time() - start_t) > last_t:
            break
    return error  

def stop(calibarr):
    pump.set_pressure(1,0,calibarr)
    pump.set_pressure(2,0,calibarr)
    pump.set_pressure(3,0,calibarr)
    pump.set_pressure(4,0,calibarr)

#-----------------------------  

def plotupdate(ax1,ax2,flow_data,active_channels,col_list,set_FR,p_range,n,k,single):
    ax1.clear()
    ax2.clear()
    chancolours = ["lightseagreen","darkorange","darkred","blueviolet"]
    for i, chan in enumerate(active_channels):
        ax1.plot(flow_data[0][n:],flow_data[1][i][n:],label="Channel %d" % chan, color=chancolours[i])
        ax2.plot(flow_data[0][n:],flow_data[2][i][n:],label="Channel %d SetP" % chan,color=chancolours[i])
        ax2.plot(flow_data[0][n:],flow_data[3][i][n:],label="Channel %d ActP" % chan,color=chancolours[i], alpha=0.5)
        if single == True:
            ax1.axhline(y=set_FR[i],color=chancolours[i],linewidth=0.5, alpha=0.5)
    if single == True:
        if len(col_list) > 0:
            ax1.axvline(x=col_list[-1],color='k',linestyle=':')
            ax2.axvline(x=col_list[-1],color='k',linestyle=':')    
    else:
        for col in col_list:        
            ax1.axvline(x=col,color='k',linestyle=':')
            ax2.axvline(x=col,color='k',linestyle=':')                    
    ax1.set_ylim(-5, np.amax(set_FR)*1.5) #np.amax(set_FR)*1.5
    ax2.set_ylim(p_range[0],p_range[1])
    ax1.legend()
    ax2.legend()
    ax1.set_ylabel('flow [uL/min]')
    ax2.set_ylabel('pressure [mbar]')
    plt.xlabel('Time (s)')
    plt.pause(0.0001)
    plt.show(block=False)


#------------------
                  
def main_PI(expname,exp_params,autocollect,active_channels,sensorcorr,period,K_p,K_i,exp_FRs,volume,tubingdim,p_range,p_incr,eqb_max,eqberror,wpdim,wpcurrent,standard_repeats,ser,calibarr):
    
    #Global variables
    flow_data,n,fdataall = [[],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]],0,[] #flow_data - time,flow,realp,setp
    pr_control, I = [0,0,0,0],[0,0,0,0]
    init_start_t = time.time()
    active = True

    #create folder for saving images
    path = './FlowData/' + expname + '/Flowplots'
    fpath = './FlowData/' + expname 
    
    records.initatefolder(path)

    #Setup live flow figure
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    fr = [0,0,0,0]

    #Iteration through each of the flow rates
    for j, set_FR in enumerate(exp_FRs): 
        
        if set_FR[0] > 0:
            FRR = set_FR[0]/np.sum(set_FR[1:])
        else:
            FRR = "0:X"
        
        repeats = 0
        expul_t = calc.expulsiontime(tubingdim,set_FR)
        print("Expulsion Travel Time:",expul_t)

        #condition_name = str(round(exp_params[1],1)) + "-" + expname + str(exp_params[2]) + str(exp_params[3]) + str(exp_params[4] )
        condition_name = str(round(FRR,1)) + "-" + expname + "-" + str(set_FR[0]) + str(set_FR[1]) + str(set_FR[2]) + str(set_FR[3] )
        
        while repeats < standard_repeats: #Gives the option to repeat a given flowrate condition
            #Set break loop for current run

            print("Beginning experiment: ", condition_name)
            print("len active chan",len(active_channels))
            fr_err_clip,error_prev = [[],[],[],[]][0:len(active_channels)],[0,0,0,0]
            print(fr_err_clip)
            collection,consistent_fr = False,True
            col_list = []

            collectionvol = volume

            if repeats > 0:
                expul_t = 2

            #Read inital time
            start_t = time.time() 
            last_t = start_t

            condition = True
            while condition == True:
                #-----Main PID Loop-----
                flow_data[0].append((time.time() - init_start_t))

                #Repeat for all active channels
                for i, channel in enumerate(active_channels):
                    #Flow rate reading
                    fr[i] = pump.get_sensor_data(channel)[0]
                    #Apply Correction
                    fr[i] = (fr[i]*sensorcorr[channel-1][0]) + sensorcorr[channel-1][1]
                    flow_data[1][i].append(fr[i])
                    #Calculate error
                    fr_error = fr[i]-set_FR[i]
                    fr_err_clip[i].append(abs(fr_error))

                    if error_prev[i]*fr_error < 0 and len(flow_data[2][i]) > 2:
                    #Perform linear interpolation
                        pr_control[i] = flow_data[2][i][-2] + (((flow_data[2][i][-1]-flow_data[2][i][-2])/(fr_error-error_prev[i]))*(0-error_prev[i]))
                        pr_control[i] = np.clip(pr_control[i], p_range[0], p_range[1])
                        flow_data[2][i].append(pr_control[i])
                    else:
                        #Correction calculations
                        I[i] = I[i] + K_i*fr_error*(period)
                        adjustment =  (fr_error*abs(fr_error))*K_p[i] + I[i]
                        #Set limits
                        adjustment = np.clip(adjustment, p_incr[0], p_incr[1])
                        pr_control[i] = pr_control[i] - adjustment 
                        pr_control[i] = np.clip(pr_control[i], p_range[0], p_range[1])
                        flow_data[2][i].append(pr_control[i])
                    #Set pressure
                    pump.set_pressure(channel,pr_control[i],calibarr)  
                    flow_data[3][i].append(pump.get_pressure_data(channel,calibarr)[0])
                    error_prev[i] = fr_error
                
                max_fr_error = np.max(list(np.max(errors) for errors in fr_err_clip))
                sd_fr_error = np.max(list((np.std(errors)) for errors in fr_err_clip))
                print("1:",fr[0],"2:",fr[1],"3:",fr[2],"4:",fr[3],"maxerror:", max_fr_error)

                if (time.time() - start_t) > expul_t and collection == False:
                    if max_fr_error < eqberror: #Absolute measure of error
                        print("FR condition reached \n\n\n")
                        #Move to well position
                        if autocollect == True:
                            expel.servoswitch(ser,1) #to collect mode
                        K_p = K_p/5
                        K_i = K_i/10
                        collection = True
                        col_list.append(time.time() - init_start_t)
                        eq_t = time.time() - start_t
                        flowstart = len(flow_data[1][0])
                        fr_err_clip = [[],[],[],[]][0:len(active_channels)]
                    elif sd_fr_error < 0.1 and (time.time() - start_t - 10) > expul_t:
                        print("ALERT---!!Blockage or Empty Reservoir!!")
                        active = False
                    for i, channel in enumerate(active_channels):
                        fr_err_clip[i] = fr_err_clip[i][1:] #Remove the first value 
    
                elif sd_fr_error > 1 and collection == True:
                    consistent_fr = False

                # Wait until desired period time
                sleep_t = period - (time.time() - last_t)
                if sleep_t > 0:
                    time.sleep( sleep_t )
                
                if collection == True:
                    collectionvol = collectionvol - (np.sum(fr)/60)*(time.time()-last_t)

                if collectionvol < 0 or (time.time()-start_t) > eqb_max:
                    if autocollect == True:
                        expel.servoswitch(ser,0) #To waste mode
                    break

                last_t = time.time()  # And update the last time

                #Updating Figure
                plotupdate(ax1,ax2,flow_data,active_channels,col_list,set_FR,p_range,n,-1,True)  

            if collection == False and condition == True :
                status = "Failed to Eq"
                eq_t = 0
                print("Equilibration Failed - FR percentage error", np.max(max_fr_error))
                repeats += -1
                flowstart = 0
            else:
                if consistent_fr == True: 
                    status = "Complete"
                    print("Collection Successful - FR percentage error", np.max(max_fr_error)) 
                    
                else:
                    status = "Failed"
                    print("Collection Unsuccessful - FR percentage error", np.max(max_fr_error)) 
                    #repeats += -1
            


            n = len(flow_data[0])-1
            ch_fr_error,mean_fr,stdev_fr = records.saveflowdata(fr_err_clip,flow_data,flowstart,fdataall,path,expname)
            records.savetoexcel(path,expname,condition_name,status,exp_params,set_FR,wpcurrent,volume,ch_fr_error,mean_fr,stdev_fr,repeats,eq_t)
            plt.savefig(path+"/"+condition_name+"-"+str(j)+"-"+str(repeats)+".png")

            #save wp positions with exp info
            wpprev = [wpcurrent[0],wpcurrent[1]]
            if wpcurrent[1] == wpdim[1]:
                wpcurrent[1] = 1
                wpcurrent[0] = wpcurrent[0] + 1
            else:
                wpcurrent[1] = wpcurrent[1] + 1

            #Move to new coordinate 
            if autocollect == True:
                threading.Thread(target=expel.nextwell,args=(ser, wpprev, wpcurrent)).start()
                print("Current plate position: ",wpcurrent)

            K_p = K_p*5
            K_i = K_i*10

            repeats+= 1
            print("repeats:",repeats,standard_repeats)
        

    plotupdate(ax1,ax2,flow_data,active_channels,col_list,exp_FRs,p_range,0,0,False)    
    plt.savefig(path+"/"+expname+"all"+".png")

    stop(calibarr) 
    if autocollect == True:
        expel.setdirection(ser,"Vert","Away")
        expel.setstep(ser,0,2000)
    
    plt.show()

    print(expname)

    return()
    


#-----------------------------------------------------------------------------------------



def ManualControl(expname,sensorcorr,period,K_p,K_i,p_range,p_incr,wpdim,wpcurrent,ser,calibarr):

    active_channels = [1,2,3,4]
    set_value = [10,20,30,10]
    mode = ["flow","pressure","flow","flow"]
    def setflowrate(channel,FR):
        print("set")
    def switchchannel(channel,state):
        print("switched")
    def setpressure(channel,PR):
        print("set")
    def resetflow():
        print("reset")
    def movewell(wellpos):
        wpprev = [wpcurrent[0],wpcurrent[1]]
        if wpcurrent[1] == wpdim[1]:
            wpcurrent[1] = 1
            wpcurrent[0] = wpcurrent[0] + 1
        else:
            wpcurrent[1] = wpcurrent[1] + 1

        #Move to new coordinate 
        threading.Thread(target=expel.nextwell,args=(ser, wpprev, wpcurrent)).start()
        print("Current plate position: ",wpcurrent)
        print("moved")
    def exit():
        stop(calibarr) 
        expel.setdirection(ser,"Vert","Away")
        expel.setstep(ser,0,2000)
        plotupdate(ax1,ax2,flow_data,active_channels,col_list,exp_FRs,p_range,0,0,False)    
        plt.savefig(path+"/"+expname+"all"+".png")
        plt.show()
        print("exit")
        active = False
    def collectionmode():
        print("collect")
        expel.servoswitch(ser,1)
        K_p = K_p/5
        K_i = K_i/10
    
    active = True

    #Global variables
    flow_data,n,fdataall = [[],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]],0,[] #time,flow,realp,setp
    pr_control, I = [0,0,0,0],[0,0,0,0]
    init_start_t = time.time()

    #create folder for saving images
    path = './FlowData/' + expname + './Flowplots'
    fpath = './FlowData/' + expname 
    
    initatefolder(path,fpath)

    #Setup live flow figure
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    ax2 = fig.add_subplot(2,1,2)
    fr,error_prev = [0,0,0,0],[0,0,0,0]

    #Read inital time
    start_t = time.time() 
    last_t = start_t

    while active == True:
        #-----Main PID Loop-----
        flow_data[0].append((time.time() - init_start_t))

        #Repeat for all active channels
        for i, channel  in enumerate(active_channels):
            #Flow rate reading
            fr[i] = pump.get_sensor_data(channel)[0]
            #Apply Correction
            fr[i] = (fr[i]*sensorcorr[channel-1][0]) + sensorcorr[channel-1][1]
            flow_data[1][i].append(fr[i])

            if mode[i] == "flow":
                fr_error = fr[i]-set_value[i]

                if error_prev[i]*fr_error < 0 and len(flow_data[2][i]) > 2:
                    #Perform linear interpolation
                    pr_control[i] = flow_data[2][i][-2] + (((flow_data[2][i][-1]-flow_data[2][i][-2])/(fr_error-error_prev[i]))*(0-error_prev[i]))
                    pr_control[i] = np.clip(pr_control[i], p_range[0], p_range[1])
                    flow_data[2][i].append(pr_control[i])
                else:
                    #Correction calculations
                    I[i] = I[i] + K_i*fr_error*(period)
                    adjustment =  (fr_error*abs(fr_error))*K_p[i] + I[i]
                    #Set limits
                    adjustment = np.clip(adjustment, p_incr[0], p_incr[1])
                    pr_control[i] = pr_control[i] - adjustment 
                    pr_control[i] = np.clip(pr_control[i], p_range[0], p_range[1])
                    flow_data[2][i].append(pr_control[i])
                #Set pressure
                pump.set_pressure(channel,pr_control[i],calibarr)  
                flow_data[3][i].append(pump.get_pressure_data(channel,calibarr)[0])
                error_prev[i] = fr_error 

            if mode[i] == "pressure":
                #Set pressure
                pump.set_pressure(channel,pr_control[i],calibarr)  
                flow_data[2][i].append(pr_control[i])
                flow_data[3][i].append(pump.get_pressure_data(channel,calibarr)[0])
                error_prev[i] = fr_error


        # Wait until desired period time
        sleep_t = period - (time.time() - last_t)
        if sleep_t > 0:
            time.sleep( sleep_t )
        last_t = time.time() # And update the last time 
        
        #Updating Figure
        plotupdate(ax1,ax2,flow_data,active_channels,col_list,set_FR,p_range,n,-1,True)    

    plt.savefig(path+"/"+condition_name+"-"+str(j)+"-"+str(repeats)+".png")
    #save wp positions with exp info

    K_p = K_p*5
    K_i = K_i*10

def PressureControl():
    print("pressure")

def ManualControl():
    print("manual")

def CleanChip():
    print("Ensure ethanol/water on all channels")    

def CleanChip():
    print("Ensure ethanol/water on all channels")


