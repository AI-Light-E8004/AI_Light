import paramiko.client
import sound
import voice_recognition
import paramiko
from scp import SCPClient
import serial 

pathname = "voice.wav"
textname = "text.txt"
destination_directory = "/scratch/work/buit8/outputText"

host = "triton.aalto.fi"
username = "buit8"
password = "aZ9r31Rdvc1W"

ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=10)
ser.reset_input_buffer()

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

if __name__ == "__main__":
    # my_sound = sound.record_microphone()
    # my_text = voice_recognition.transcribe_audio_path(pathname)
    # print(my_text)

    # ssh = createSSHClient(host,22,username,password)
    # scp = SCPClient(ssh.get_transport())
    # scp.put(textname,destination_directory)
