#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        # ser.write(b"1\n")
        if ser.in_waiting > 0:
            line = ser.readline().rstrip()
            print(line)
        # time.sleep(10)
        # ser.write(b"2\n") 
        # if ser.in_waiting > 0:
        #     line = ser.readline().rstrip()
        #     print(line)
        # time.sleep(10)
        # ser.write(b"3\n")
        # if ser.in_waiting > 0:
        #     line = ser.readline().rstrip()
        #     print(line)
        # time.sleep(10)
        # ser.write(b"4\n") 
        # if ser.in_waiting > 0:
        #     line = ser.readline().rstrip()
        #     print(line)
        # time.sleep(10)