#FRR
FRR_range = range(1,10+1,1) #[min,max,increment]

#Channel - Buffer 
Buff_Active = True
Buffer_FR_range = range(180,180+1,20)

#Channel 2 - Lipid 1 in ethanol 
Lp1_Active = True #Is there a input on Ch2?
Lp1_Lipid = "Lipid1_Name"
Lp1_Lipid_Mr = 100 #Molecular Weight of Lipid 1
Lp1_Lipid_Range = "Base" 
Lp1_Lipid_Conc = 10 #(mg/ml)

#Channel 3 - Lipid 2 in ethanol 
Lp2_Active = True #Is there a input on Ch3?
Lp2_Lipid = "Lipid2_Name"
Lp2_Lipid_Mr = 50 #Molecular Weight of Lipid 2
Lp2_Lipid_Range = range(0,(10+1),5) #Compositional Range [min,max,increment]
Lp2_Lipid_Conc = 5 #(mg/ml)
Lp2_Lipid_Mr_Ratio = Lp1_Lipid_Mr/Lp2_Lipid_Mr

#Channel 4 - Lipid 3 in ethanol 
Lp3_Active = True #Is there a input on Ch4?
Lp3_Lipid = "Lipid3_Name"
Lp3_Lipid_Mr = 50 #Molecular Weight of Lipid 3
Lp3_Lipid_Range = range(0,(10+1),5) #Compositional Range [min,max,increment]
Lp3_Lipid_Conc = 5 #(mg/ml)
Lp3_Lipid_Mr_Ratio = Lp1_Lipid_Mr/Lp3_Lipid_Mr


exp_params, flow_rate  = [],[]
n = 0

if Buff_Active == True and Lp1_Lipid_Range == "Base":
    for buffer_FR_total in Buffer_FR_range: 
        for FRR_value in FRR_range:
            lipid_FR_total = buffer_FR_total/FRR_value
            for a in Lp2_Lipid_Range:
                for b in Lp3_Lipid_Range:
                    Lp1_const = (((100-a-b)/1000))/(Lp1_Lipid_Conc*0.001)
                    Lp2_const = ((a/1000)*Lp2_Lipid_Mr_Ratio)/(Lp2_Lipid_Conc*0.001)
                    Lp3_const = ((b/1000)*Lp3_Lipid_Mr_Ratio)/(Lp3_Lipid_Conc*0.001)
                    FR_const = Lp1_const + Lp2_const + Lp3_const
                    Lp1_flow_rate = (Lp1_const/FR_const)*lipid_FR_total 
                    Lp2_flow_rate = (Lp2_const/FR_const)*lipid_FR_total 
                    Lp3_flow_rate = (Lp3_const/FR_const)*lipid_FR_total 
                    totalFR = buffer_FR_total + lipid_FR_total
                    exp_params.append([totalFR,FRR_value,100-a-b,a,b])
                    flow_rate.append([buffer_FR_total,Lp1_flow_rate,Lp2_flow_rate,Lp3_flow_rate])
                    n=n+1

print(exp_params)
print(flow_rate)
print(len(exp_params),len(flow_rate))