import os
import sys
import serial
import serial.tools.list_ports
from datetime import datetime
import matplotlib.pyplot as plt
import time


def serconnect():
    global ser
    setupstring = ""
    ports = serial.tools.list_ports.comports()
    for p in ports:
        print(p)
    serialport = str(p.device)  # just takes the port - i.e. COM3
    print(serialport)
    ser = serial.Serial(
        serialport, baudrate=115200, timeout=30
    )  # then updates ser to take into account serial port
    print("Connected to " + serialport + "\n")
    #for i in range(3):
    b = ser.readline()  # used if know input terminated with EOL characteres
    readstring = b.decode("utf-8")
    setupstring += readstring
    return ser

def setdirection(ser,axis,direction):
    if direction == "Towards":
        direction = 1
    elif direction == "Away":
        direction = 0

    if axis == "Horz":
        expected_message = 'Turnt1'
        writestring = '<M'+str(direction)+'>' #M is defined to set motor 1 direction in Arduino
        bytestowrite = writestring.encode() #encodes the string to UTF-8
        ser.write(bytestowrite) # sending the data

    if axis == "Vert":
        expected_message = 'Turnt2'
        writestring = '<N'+str(direction)+'>' #M is defined to set motor 1 direction in Arduino
        bytestowrite = writestring.encode() #encodes the string to UTF-8
        ser.write(bytestowrite) # sending the data

def setstep(ser,stepsH,stepsV):
    writestring = "<B" + str(stepsH) + "," + str(stepsV) + ">"
    bytestowrite = writestring.encode()  # encodes the string to UTF-8
    ser.write(bytestowrite)  # sending the data
    b = ser.readline()
    readstring = b.decode("utf-8")

def move(ser,dirH,dirV,stepsH,stepsV):
    setdirection(ser,"Vert", dirV)
    setdirection(ser,"Horz", dirH)
    setstep(ser,stepsH,stepsV)

def home(ser):
    #Home Axes
    move(ser,"Away","Away", 100, 100)
    writestring = '<H>' #M is defined to set motor 1 direction in Arduino
    bytestowrite = writestring.encode() #encodes the string to UTF-8
    ser.write(bytestowrite) # sending the data
    b = ser.readline()
    readstring = b.decode("utf-8")
    #print(readstring)
    setdirection(ser,"Vert","Away")
    setdirection(ser,"Horz","Away")

def homeandfirst(ser):
    print("To home and first well")
    home(ser)
    setstep(ser,1650,800)


def nextwell(ser,wpprev,wpcurrent): #current is the next one, prev is the current lel
    vstep = 1675/(7)*(wpcurrent[0]-wpprev[0])
    hstep = 2637.5/(11)*(wpcurrent[1]-wpprev[1])
    print(vstep,hstep)
    if vstep > 0:
        dirV = "Away"
    else:
        dirV = "Towards"
    if hstep > 0:
        dirH = "Away"
    else:
        dirH = "Towards"    
    move(ser,dirH,dirV,hstep,vstep)


def currenttowait(ser,wpcurrent):
    vstep = 3350/(7)*(wpcurrent[0]-1)
    hstep = 5275/(11)*(wpcurrent[1]-1)
    move(ser,"Towards","Towards",hstep,vstep+1100)

    homeandwaste(ser)
    wastetowell(ser,[6,8])
    currenttowaste(ser,[6,8])
    wastetowell(ser,[2,3])
    currenttowaste(ser,[2,3])

def nextwellold(ser):  
    #Total well step length 5300H 3400V - NUNC 12x8 well plate
    #Ordered pathway - Rows - columns 
    rows = 8
    cols = 12
    hstep = 5275/(cols-1)
    vstep = 3350/(rows-1)
    for i in range(0,rows):
        for j in range(0,cols-1):
            move(ser,"Horz","Away",hstep)
            time.sleep(3)
        move(ser,"Horz","Towards",5275)
        move(ser,"Vert","Away",vstep)
    move(ser,"Vert","Towards",3350+hstep)

def flowswitch(ser,state): #State is 0 or 1 
    if state == 0:
        writestring = '<F'+str(state)+'>' #M is defined to set motor 1 direction in Arduino
        bytestowrite = writestring.encode() #encodes the string to UTF-8
        ser.write(bytestowrite) # sending the data
    elif state == 1:
        writestring = '<F'+str(state)+'>' #M is defined to set motor 1 direction in Arduino
        bytestowrite = writestring.encode() #encodes the string to UTF-8
        ser.write(bytestowrite) # sending the data
    