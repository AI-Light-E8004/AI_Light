from mutagen.mp3 import MP3 
from PIL import Image 
from pathlib import Path 
import os 
import imageio 
from moviepy import editor 

audio_path = os.path.join(os.getcwd(), "./music/music.mp3") 
video_path = os.path.join(os.getcwd(), "videos") 
images_path = os.path.join(os.getcwd(), "images") 
audio = MP3(audio_path) 
audio_length = audio.info.length 

list_of_images = [] 
for image_file in os.listdir(images_path): 
    if image_file.endswith('.png') or image_file.endswith('.jpg'): 
        image_path = os.path.join(images_path, image_file) 
        image = Image.open(image_path)
        list_of_images.append(image)

# Create a list to hold the blended frames
blended_images = [list_of_images[0]]

# Blend each frame with the previous one with a fading effect
for i in range(1, len(list_of_images)):
    previous_image = blended_images[-1]
    current_image = list_of_images[i]
    
    # Define a sequence of intermediate images for smooth transition (fading)
    num_steps = 40  # Adjust the number of steps for smoother or faster fading
    for j in range(1, num_steps + 1):
        alpha = j / num_steps
        blended_image = Image.blend(previous_image, current_image, alpha=alpha)
        blended_images.append(blended_image)

duration = audio_length / len(blended_images) 
imageio.mimsave('images.gif', blended_images, fps=1/duration) 

video = editor.VideoFileClip("images.gif") 
audio = editor.AudioFileClip(audio_path) 
final_video = video.set_audio(audio) 
os.chdir(video_path) 
final_video.write_videofile(fps=60, codec="libx264", filename="video.mp4")
