import numpy as np
import pump 
import control
import flow_calculator as calc
import expel
import records

#----------------------------------Record Keeping------------------------------------------
record = False

ExpTitle = "Flush"
Details = "5FRR"
BufferName = "TRIS-Calcein"
BufferNotes = "TRIS-pH-7.61 with 6mM Calcein"
Lp1Name = "DOPC"
Lp1Notes = "10mg/ml DOPC in Ethanol 99.5% Pure - MHF Stock"
Lp2Name = "N/A"
Lp2Notes = "N/A"
Lp3Name = "N/A"
Lp3Notes = "N/A"

#----------------------------------Experiment Parameters-----------------------------------
#Mode = "Composition"
Mode = "FlowControl"  #Only fill in your chosen section below

if Mode == "Composition":
    #FRR
    FRR_range = range(1,10+1,1) #[min,max,increment]

    #load compositions from doc  

    #Channel 1 - Buffer 
    Buffer = [BufferName,True, range(60,60+1,20)]

    #Channel 2 - Lipid 1 in ethanol
    #Lp1=[Name, MW, Range , Concentration]  
    Lp1 = [Lp1Name, 100, "Base",  10]  

    #Channel 3 - Lipid 2 in ethanol - if not active, set range to 0
    #Lp2= [Name, MW, Range , Concentration]  
    Lp2 = [Lp2Name, 50, range(0,(10+1),5), 5]  

    #Channel 4 - Lipid 3 in ethanol - if not active, set range to 0
    #Lp3= [Name, MW, Range , Concentration]  
    Lp3 = [Lp3Name, 50, range(0,(10+1),5), 5]   

    exp_params,exp_FRs = calc.flow_calc(FRR_range,Buffer,Lp1,Lp2,Lp3)
    print(exp_FRs)

elif Mode == "FlowControl":
    exp_FRs = [[60,60,0,0],[100,20,0,0],[100,20,0,0]]
    Buffer,Lp1,Lp2,Lp3 = None,None,None,None
    exp_params = calc.genparams(exp_FRs)

elif Mode == "Manual Control":
    print("Manual")

#----------------------------------General Parameters------------------------------------------   
inst_name = '0204B3ED'
#Sensor setup [Channel, Type (5-1000uL/min)(4-80uL/min) , Digital (1), Calibration (H20 -0), Pixel (7) ]
sensor1 = [1,5,1,0]#[1,4,1,0]
sensor2 = [2,5,1,0]  ##IMPORTANT Change calibration if using MFS3 sensor - control.py PID
sensor3 = [3,5,1,0]
sensor4 = [4,5,1,0]
sensorcorr = [[1.1183,-6.4631],[1.8076,-7.9951],[1.7487,-9.2466],[1.9081,-7.7105]] #Sensor calibration corrections

#PI Controller Parameters
period = 0.3
K_p = np.array([50,30,30,30]) #Tune the proportional component 0.018 [0.02,0.01,0.01,0.01]#[0.04,0.008,0.008,0.008]65um[200,30,30,30]
K_i = 0.0001 #Tune the integral component  0.0005 65um 0.0001
p_incr = [-500,500] #min,max 65um [-500,500]
p_range = [0,2000] #min,max 65um [0,2000]

#----------------------------------Autocontroller Parameters-----------------------------------
active_chans = [1,2] #Set all active channels  [1,2,3,4]  FIX THE ERROR IN RECORDS

volume = 100 #volume collected in micro litres

tubingdim = [0.51,100] #dim,length of the final tubing in mm 

#Repeats
standard_repeats = 3  #How many tines should each composition be repeated
fail_repeats = 1 #If FR falls out of range, how many repeats 

#Experiment timings
max_equilibration_t = 120 #Maximum time to reach FR equilibrium

#Equilibrium Conditions
Eqabserror = 1.5 #Maximum absolute error in flow rate over equilbiriation time 

#Autocollect Configuration 
autocollect = False
autohome = False #Set to False if autocollecting but dont need to rehome - i.e already over the first well
wpdim = [8,12] #row col
wpcurrent = [5,1] #set this as the first well to be used

#----------------------------------Initiation-----------------------------------PUT THIS IN A FUNCTION
error = [] #Error Handling
ser = expel.initialise(autocollect,autohome,wpcurrent)
error.append(pump.pressure_init())
calibarr,errora = pump.pressure_calib("load")
error.append(errora)
error.append(pump.sensor_init(sensor1, sensor2, sensor3, sensor4))
#error = control.flush(active_chans,100,(0.1*60),calibarr) #pressure 

if np.max(error) == 0:
    #---------------------------------Record Keeping------------------------------- PUT THIS IN A FUNCTION 
    if record == True:
        expname = records.saverecord(ExpTitle,Details,Mode,BufferName,Buffer,BufferNotes,Lp1Name,Lp1,Lp1Notes,Lp2Name,Lp2Notes,Lp2,Lp3Name,Lp3Notes,Lp3,exp_params,exp_FRs,inst_name,active_chans,sensorcorr,volume,standard_repeats,fail_repeats,period,K_p,K_i,p_incr,p_range,max_equilibration_t,Eqabserror)
    else:
        expname = "Test"

    #---------------------------------Main Loop------------------------------------
    main_loop = True
    if main_loop == True:
        control.main_PI(expname,exp_params,autocollect,active_chans,sensorcorr,period,K_p,K_i,exp_FRs,volume,tubingdim,p_range,p_incr,max_equilibration_t,Eqabserror,wpdim,wpcurrent,standard_repeats,ser,calibarr)
        #--------------------------------Functions------------------------------------------
