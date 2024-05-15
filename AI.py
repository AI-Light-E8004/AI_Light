import paramiko.client
import sound
import voice_recognition
import paramiko
from scp import SCPClient
import serial 
import cv2, numpy as np 
from sklearn.cluster import KMeans
import time 

pathname = "voice.wav"
textname = "text.txt"
destination_directory = "/scratch/work/buit8/outputText"

host = "triton.aalto.fi"
username = "buit8"
password = "aZ9r31Rdvc1W"



def visualize_colors(cluster, centroids):
    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins = labels)
    hist = hist.astype("float")
    hist /= hist.sum()

    # Create frequency rect and iterate through each cluster's color and percentage
    rect = np.zeros((50, 300, 3), dtype=np.uint8)
    colors_percent = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
    colors = [x[1] for x in colors_percent]
    
    return colors


def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

if __name__ == "__main__":
    ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=10)
    ser.reset_input_buffer()
    # # capture sound from microphone 
    

    # #placing file into the server 
    # ssh = createSSHClient(host,22,username,password)
    # scp = SCPClient(ssh.get_transport())
    # scp.put(textname,destination_directory)

    # Load image and convert to a list of pixels 
    image = cv2.imread('testimage4.jpeg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    reshape = image.reshape((image.shape[0] * image.shape[1], 3))
    
    cluster = KMeans(n_clusters=5).fit(reshape)
    colors = visualize_colors(cluster, cluster.cluster_centers_)
    # colors is the group of 5 color as array of 3 number, representing rgb 
    color_string = ""
    for color in colors:
        int_color = np.array([round(i) for i in color])
        for rgb in int_color:
            color_string += str(rgb)
            color_string += " "
        color_string += ";"
    color_string = color_string[:-1]
    color_string += '\n'
    print(color_string)
    time.sleep(1)
    while True:
        ser.write (color_string.encode())
        line = ser.readline().decode('utf-8').rstrip()
        if line == '1':
            print("prepare to record")
            time.sleep(1.5)
            my_sound = sound.record_microphone()
            my_text = voice_recognition.transcribe_audio_path(pathname)
            print(my_text)