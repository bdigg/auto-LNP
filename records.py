import numpy as np
from datetime import datetime


def id():
    previd = np.load("C:/Users/bdigg/OneDrive/Documents/GitHub/auto-LNP/auto-LNP/id.npy")
    id = previd + 1
    return id

def date():
   now = datetime.now() 
   date = now.strftime("%y%m%d")

   print(date)
   return date

def time():
    now = datetime.now() 
    time = now.strftime("%H:%M:%S")
    print(time)
    return time