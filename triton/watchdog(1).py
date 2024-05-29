import os
import subprocess
import time

# Path to the WAV file
file_path = "./outputText/text.txt"

# Initial modification time of the file
prev_modification_time = os.path.getmtime(file_path)

while True:
    # Get the current modification time of the file
    current_modification_time = os.path.getmtime(file_path)
    
    # If the modification time has changed, run sbatch Auto.sh
    if current_modification_time != prev_modification_time:
#         subprocess.run(["python", "audio-to-text.py"])
#         print("audio-to-text.py done!")
        subprocess.run(["python", "text-video-v5.py"])
        print("text-video-v5.py done!")
        subprocess.run(["python", "merge-image-music-v1.py"])
        print("merge-image-music-v1.py done!")
        
        # Update the previous modification time
        prev_modification_time = current_modification_time
        
    # Wait for some time before checking again (e.g., every 5 seconds)
    time.sleep(1)