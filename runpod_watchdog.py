import os
import subprocess
import time

# Path to the WAV file
file_path = "/workspace/Open-Sora/assets/texts/t2v.txt"

# Initial modification time of the file
prev_modification_time = os.path.getmtime(file_path)

while True:
    print
    # Get the current modification time of the file
    current_modification_time = os.path.getmtime(file_path)
    
    # If the modification time has changed, run sbatch Auto.sh
    if current_modification_time != prev_modification_time:
        print("received request")
        print("starting video generation")
        subprocess.run(["python", "/workspace/Open-Sora/scripts/inference.py", "/workspace/Open-Sora/configs/opensora-v1-2/inference/sample.py"
                        , "--num-frames", "4s", "--resolution", "480p", "--aspect-ratio", "1:1"
                        , "--prompt-path", "/workspace/Open-Sora/assets/texts/t2v.txt"])
        print("video generation done!")
        
        # Update the previous modification time
        prev_modification_time = current_modification_time
        
    # Wait for some time before checking again (e.g., every 5 seconds)
    time.sleep(2)