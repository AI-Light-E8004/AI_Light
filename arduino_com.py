import paramiko.client
import sound
import voice_recognition
import paramiko
from scp import SCPClient
import serial 
import cv2, numpy as np 
from sklearn.cluster import KMeans
import time 
import subprocess
import os
import vlc

my_string = "14"
if __name__ == "__main__":
    ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0.1)
    ser.reset_input_buffer()
    while True:
        with open('light_state.txt' , 'r') as file:
            my_string = file.read()
        print("mystring is: " + str(my_string))
        ser.write(int(my_string).to_bytes(1, 'big'))
        loopback = ser.read()
        print(loopback)
        # time.sleep(1)        
        ser.reset_input_buffer()
        # ser.flush()
