import serial
import serial.tools.list_ports
import time
from Connections import SerialConnections
from TwoMotorControl import MotorControl
from Actuatormovement import MovementandSaving


int_time = 80
serial_connection = SerialConnections(int_time)
spec = serial_connection.spectrometerConnection()
ser = serial.Serial('COM10', baudrate=115200, timeout=30)
print('connected')
setupstring = ''
for i in range(1):
    b = ser.readline() #used if know input terminated with EOL characteres
    readstring = b.decode("utf-8")
    setupstring+=readstring
    print(setupstring)
time.sleep(5)
top_motor = MotorControl(2,ser)
bottom_motor = MotorControl(1, ser)


folder_name ='Niall_Test_LS_1045'
movement = MovementandSaving(20,2,4, folder_name, 0.2, spec, r'D:\OneDrive - Imperial College London\Year1PhD\Motor_Calibration_With_AccelLib')
#movement.makeFolders()




movement.multipleHoming(bottom_motor, top_motor)

#movement.movementForExperiment(bottom_motor, top_motor)
#movement.movementAndSaving(bottom_motor, top_motor, (20), (167), (83), (83*3))