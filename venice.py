
import paramiko
import sound
import time 
import subprocess
import os
import voice_recognition
import paramiko
from scp import SCPClient

pathname = "voice.wav"
textname = "text.txt"

username = 'root'
ip = '91.199.227.82'   #change IP address accordingly 
port = 12308          #change port accordingly 
key_path = '/home/tung/.ssh/id'  # path to private key 

local_path = 'text.txt'
# local_path = "runpod_watchdog.py"
remote_path = '/workspace/Open-Sora/assets/texts/t2v.txt'
# remote_path = 'workspace/Open-Sora/runpod_watchdog.py'
def ssh_client(username, ip, port, key_path):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=username, key_filename=key_path)
    return client

def send_file(client, local_path, remote_path):
    with SCPClient(client.get_transport()) as scp:
        scp.put(local_path, remote_path) 

def add_style(text):
    style1 = "Black on white, line sketching"
    style2 = "Colorful, cartoonish"
    style3 = "Mystic, dark"
    final_text = text + "." + style1
    return final_text

if __name__ == "__main__":
    my_sound = sound.record_microphone()
    my_text = voice_recognition.transcribe_audio_path(pathname)
    print(my_text)
    print(add_style(my_text))

    client = ssh_client(username, ip, port, key_path)

    send_file(client, local_path, remote_path) # to be tested 

    # scp = SCPClient(ssh.get_transport())
    # scp.put(textname,destination_directory)