import serial
import time
def SendCommandToArduino(com: str):
    sr = serial.Serial(port='COM4',  baudrate=115200, timeout=.1)
    sr.write((bytes(com,  'utf-8')))
    time.sleep(0.1)
    return 'Sent'