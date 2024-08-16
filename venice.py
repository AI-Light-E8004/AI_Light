
import paramiko
import sound
import time 
import subprocess
import os
import voice_recognition
import paramiko
from scp import SCPClient
import serial

pathname = "voice.wav"
textname = "text.txt"

username = 'root'
ip = '69.30.85.156'   #change IP address accordingly 
port = 22049          #change port accordingly 
key_path = '/home/tung/.ssh/id'  # path to private key 

local_path = 'text.txt'
remote_path = '/workspace/Open-Sora/assets/texts/t2v.txt'
backup_folder_path = '/home/tung/Desktop/Master/AI_Light/backup/'

def ssh_client(username, ip, port, key_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=username, key_filename=key_path)
    return client

def send_file(client, local_path, remote_path):
    with SCPClient(client.get_transport()) as scp:
        scp.put(local_path, remote_path) 

# FUNCTION4: Generate the next filename with a running number in the specified directory.
def get_next_filename(path, prefix, extension):
    existing_files = [f for f in os.listdir(path) if f.startswith(prefix) and f.endswith(extension)]
    if not existing_files:
        return f"{prefix}0000{extension}"
    existing_files.sort()
    last_file = existing_files[-1]
    last_number = int(last_file[len(prefix):-len(extension)])
    next_number = last_number + 1
    return f"{prefix}{next_number:04d}{extension}"




if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    
    while True:
        
        if ser.in_waiting > 0:
            line = ser.readline().decode().rstrip()
            print(line)
            if line[0] == '5':
                print("sound recording command received")
                time.sleep(1)
                my_sound = sound.record_microphone()
                try:   
                    my_text = voice_recognition.transcribe_audio_path(pathname)
                except:
                    print("could not detect any sound")
                backup_name = get_next_filename(backup_folder_path, 'text', '.txt')
                file_directory = backup_folder_path + backup_name
                f = open(file_directory, "w")
                f.write(my_text)

            # client = ssh_client(username, ip, port, key_path)
            # send_file(client, local_path, remote_path) 
            time.sleep(1)
            ser.reset_input_buffer()
            ser.reset_output_buffer()

