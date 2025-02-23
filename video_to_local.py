import paramiko
import time
import subprocess
import os
import vlc
from scp import SCPClient

# Remote server details
username = 'root'    
ip = '69.30.85.162'   #change IP address accordingly 
port = 22198         #change port accordingly 
key_path = '/home/tung/.ssh/id_ed25519'   # path to private ssh ed25519 key

# Paths to correct folders
remote_file_path = '/workspace/Open-Sora/samples/samples/sample_0000.mp4'         # Output file of the AI model
local_file_path = '/home/tung/Desktop/Master/AI_Light/sample_outputs/'                                    # Destination file path where video is stored on local for playback
backup_folder_path = '/home/tung/Desktop/Master/AI_Light/backup_outputs'       # Destination file path where every output is stored
video_file_path = '/home/aiproject/Project/sample_outputs/sample_0000.mp4' 
polling_video_path = '/home/tung/Desktop/Master/AI_Light/polling_video/video.mp4'
status_file = "light_state.txt"
status_written = False                                 

# Define loop count for video playback
loop_count_idle = 1 #4s loop 
loop_count_video = 15 #1 minute video
max_retries = 5

# FUNCTION1: Establish an SSH connection to the remote server.
def ssh_client(username, ip, port, key_path):
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try:
    client.connect(ip, port, username=username, key_filename=key_path)
    print("SSH Connection successful.")
  except Exception as e:
      print(f"SSH connection failed: {e}")
  return client

# FUNCTION2: Get the last modification time of the file on the remote server.
def get_update_time(client, path):
  stdin, stdout, stderr = client.exec_command(f'stat -c %Y {path}' )

  update_time = stdout.read().strip()
  error_msg_poll = stderr.read().strip()

  if error_msg_poll:
    raise Exception(f"Error getting modification time: {error_msg_poll}")

  return int(update_time)

def get_file_size(client, path):
  stdin, stdout, stderr = client.exec_command(f'stat -c %s {path}' )

  file_size = stdout.read().strip()
  error_msg_size = stderr.read().strip()

  if error_msg_size:
    raise Exception(f"Error getting file size: {error_msg_size}")

  return int(file_size)

# FUNCTION3: Transfer the file from the remote server to the local machine.
def file_transfer(client, remote_path, local_path):
  with SCPClient(client.get_transport()) as scp:
    scp.get(remote_path, local_path)
    print("File downloaded successfully.")

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

# FUNCTION5: Verify video data using ffmpeg
def verify_video(file_path):
  try:
    subprocess.run(['ffmpeg', '-v', 'error', '-i', file_path, '-f', 'null', '-'], check=True)
    print("Video verification successful.")
    return True
    
  except subprocess.CalledProcessError as e:
    print(f"Video verification failed: {e}")
    return False

# FUNCTION6: Play the video file using MPV, looping it the specified number of times.
def play_video(file_path, loop_count):
  
  print("Playing a video...")

  time.sleep(5)
  subprocess.run(['mpv', '--loop=' + str(loop_count), '--fs', file_path, '--fs-screen=0'], check=True)
  
  print("Finished playing the video.")

# Establish SSH client connection
client = ssh_client(username, ip, port, key_path)

# Initial modification time of the file
prev_update_time = get_update_time(client, remote_file_path)
prev_file_size = get_file_size(client, remote_file_path)

while True:
  if not status_written:
    with open(status_file, 'w') as f:
      f.write("1\n")
    status_written = True
    
  print("Polling the server for file updates...")
  curr_update_time = get_update_time(client, remote_file_path)
  curr_file_size = get_file_size(client, remote_file_path)
  
  if curr_update_time != prev_update_time and curr_file_size != prev_file_size:
    time.sleep(5)
    retries = 0
    
    while retries < max_retries:
      local_full_path = os.path.join(local_file_path, os.path.basename(remote_file_path))  # Construct the full local path for the file
      file_transfer(client, remote_file_path, local_full_path)  # Transfer the file from the remote server to the local path
      if verify_video(local_full_path):
        print("Verification successful.")
        break
      else:
        print("Verification failed, retrying transfer...")
        retries += 1
        time.sleep(2)
        
        if retries == max_retries:
          print("Failed to transfer and verify the file after multiple attempts.")
          continue

    next_backup_filename = get_next_filename(backup_folder_path, 'sample_', '.mp4')         # Generate the next backup filename with a running number
    backup_full_path = os.path.join(backup_folder_path, next_backup_filename)
    print(f"Backing up file from {local_full_path} to {backup_full_path}")
    
    subprocess.run(['cp', local_full_path, backup_full_path], check=True)
    print(f"Video file copied to backup: {backup_full_path}")
    
    with open(status_file, 'w') as f:
      f.write("4\n")
    
    play_video(local_full_path, loop_count_video)                                                 # Play the file using MPV, loop it loop_count times
    
    time.sleep(10) # Wait for 10 seconds before the next check
    prev_update_time = curr_update_time                                                     # Update the previous update time to the current update time
    prev_file_size = curr_file_size
    status_written = False
  
  else:
    # time.sleep(5)                                                                           # Wait for 5 seconds before the next check if the file hasn't been updated
    # subprocess.run(['mpv','--no-terminal', '--really-quiet', '--fs',polling_video_path])
     subprocess.run(['mpv', '--loop=' + str(loop_count_idle), '--fs', polling_video_path,'--fs-screen=0'])
