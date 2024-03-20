### Niall McIntyre Connection

import os
import sys

from ctypes.wintypes import LONG
from pickletools import long1

import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from IPython import display
import time
import threading


class SerialConnections:
    def __init__(self, integration_time):
        self.integration_time = integration_time

    def setUpSerialPort(self):
        """
        Establishes the serial connection between the computer (controlled via a Jupyter notebook) and the Arduino microcontroller.
        """
        global ser
        setupstring = ""
        ports = serial.tools.list_ports.comports()
        for p in ports:
            print(p)
        serialport = str(p.device)  # just takes the port - i.e. COM3
        print(serialport)
        ser = serial.Serial(
            serialport, baudrate=115200, timeout=2
        )  # then updates ser to take into account serial port
        print("Connected to " + serialport + "\n")
        for i in range(3):
            b = ser.readline()  # used if know input terminated with EOL characteres
            readstring = b.decode("utf-8")
            setupstring += readstring
        print(setupstring)

if __name__ == "__main__":
    serial_conn = SerialConnections(200)
    serial_conn.spectrometerConnection()