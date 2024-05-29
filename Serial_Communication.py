import serial
import time
import struct 

values = "hello"
values_as_bytes = str.encode(values)
# for i in values:
#     string += struct.pack('!B', i)

ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=10)
ser.reset_input_buffer()

print("connected to: " + ser.portstr)
count=1

while True:
    ser.write(b"100,124,155;121,122,123;123,124,125;111,121,131!\n")
    # time.sleep(100)
    # receive = ser.read()
    # if ser.in_waiting > 0:
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    # time.sleep(1)