import pressure as press
import time

pstate = False

reagents = ["None","DPPC","DOPC","LysoPC","Chol","Buffer"]
def main_loop():
    while True:
        print("main loop")
        time.sleep(1)


def setup_initiate():
    print("Initialising Setup")
    if pstate == True:
        press.pressure_init()
    #Grey out button after initalisation 

def setup_calib(calibsetting):
    print("Calibrate button clicked:", calibsetting)
    if pstate == True:
        press.pressure_calib(calibsetting)


def setup_ch1(Reagent,Conc,Vol):
    print(Reagent,Conc,Vol)
    
def setup_ch2(Reagent,Conc,Vol):
    print(Reagent,Conc,Vol)
    
def setup_ch3(Reagent,Conc,Vol):
    print(Reagent,Conc,Vol)

def setup_ch4(Reagent,Conc,Vol):
    print(Reagent,Conc,Vol)

def exp_ch1(Flow):
    print(Flow)
    
def exp_ch2(Flow):
    print(Flow)
    
def exp_ch3(Flow):
    print(Flow)

def exp_ch4(Flow):
    print(Flow)