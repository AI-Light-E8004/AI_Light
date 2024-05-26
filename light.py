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

pathname = "voice.wav"
textname = "text.txt"
destination_directory = "/scratch/work/buit8/outputText"

imageName = "frame_pirate.jpeg"
VIDEOPATH = 'video_pirate.mp4'

host = "triton.aalto.fi"
username = "buit8"
password = "aZ9r31Rdvc1W"


VIDEOLENGTH = 30
COLOR_OFF = "0 0 0; 0 0 0; 0 0 0; 0 0 0; 0 0 0"
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

def get_rgb_from_image(imageName):
    image = cv2.imread(imageName)
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
    return color_string

if __name__ == "__main__":
    ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=10)
    ser.reset_input_buffer()

# Load image and convert to a list of pixels 
    

    # image = cv2.imread(imageName)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # reshape = image.reshape((image.shape[0] * image.shape[1], 3))
    
    # cluster = KMeans(n_clusters=5).fit(reshape)
    # colors = visualize_colors(cluster, cluster.cluster_centers_)
    # # colors is the group of 5 color as array of 3 number, representing rgb 
    # color_string = ""
    # for color in colors:
    #     int_color = np.array([round(i) for i in color])
    #     for rgb in int_color:
    #         color_string += str(rgb)
    #         color_string += " "
    #     color_string += ";"
    # color_string = color_string[:-1]
    # color_string += '\n'
    # print(color_string)
    # time.sleep(1)
    cap = cv2.VideoCapture(VIDEOPATH)
    # while cap.isOpened():
    #     ret, frame = cap.read()

    media_player = vlc.MediaPlayer() 
    media_player.toggle_fullscreen()
    media = vlc.Media(VIDEOPATH)
    media_player.set_media(media)
    media_player.play()
    current_time = time.time()

    while time.time() < current_time + VIDEOLENGTH: 
        color_string = get_rgb_from_image(imageName)
        ser.write (color_string.encode())
        time.sleep(1.5)
    
    ser.write(COLOR_OFF.encode())
    time.sleep(1)
    ser.write(COLOR_OFF.encode())
    time.sleep(1)