import paramiko
import time
import subprocess
import os
import vlc
from scp import SCPClient

# Remote server details
username = 'root'    
ip = '205.196.17.50'                 # <-- ADD IP-ADDRESS OF REMOTE HOST
port = 8875                            # <-- ADD PORT OF REMOTE HOST
key_path = '/home/aiproject/ssh/id_ed25519'   # path to private ssh ed25519 key

# Paths to correct folders
remote_file_path = '/workspace/Open-Sora/samples/samples/sample_0000.mp4'         # Output file of the AI model
local_file_path = '/home/aiproject/Project/sample_outputs/'                                    # Destination file path where video is stored on local for playback
backup_folder_path = '/home/aiproject/Project/backup_outputs'       # Destination file path where every output is stored
video_file_path = '/home/aiproject/Project/sample_outputs/sample_0000.mp4'                                  

# Define loop count for video playback
loop_count = 3

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
    
def start_pulseaudio():
  try:
    subprocess.run(['pulseaudio', '--check'], check=True)
    print("PulseAudio is already running.")
  except subprocess.CalledProcessError:
    try:
      subprocess.run(['pulseaudio', '--start'], check=True)
      print("PulseAudio started successfully.")
    except subprocess.CalledProcessError as e:
      print(f"Failed to start PulseAudio: {e}") 
      
def start_dbus():
  try:
    subprocess.run(['pgrep', 'dbus-daemon'], check=True)
    print("D-Bus is already running.")
  except subprocess.CalledProcessError:
    try:
      subprocess.run(['dbus-launch'], check=True)
      print("D-Bus started successfully.")
    except subprocess.CalledProcessError as e:
      print(f"Failed to start PulseAudio: {e}")

# FUNCTION5: Play the video file using MPV, looping it the specified number of times.
def play_video(file_path, loop_count):
  start_dbus()
  start_pulseaudio()
  print("Playing a video...")

  time.sleep(15)
  subprocess.run(['mpv', '--loop=' + str(loop_count), '--fs', file_path], check=True)
  
  print("Finished playing the video.")




############################# STILL PROBLEM WITH PLAYING VIDEO, FOR SOME REASON VIDEO LOSES METADATA#######################




# Establish SSH client connection
client = ssh_client(username, ip, port, key_path)


# Initial modification time of the file
prev_update_time = get_update_time(client, remote_file_path)

while True:
  print("Polling the server for file updates...")
  curr_update_time = get_update_time(client, remote_file_path)
  
  if curr_update_time != prev_update_time:
    
    local_full_path = os.path.join(local_file_path, os.path.basename(remote_file_path))     # Construct the full local path for the file
    file_transfer(client, remote_file_path, local_full_path)                                # Transfer the file from the remote server to the local path

    next_backup_filename = get_next_filename(backup_folder_path, 'sample_', '.mp4')         # Generate the next backup filename with a running number
    backup_full_path = os.path.join(backup_folder_path, next_backup_filename)
    print(f"Backing up file from {local_full_path} to {backup_full_path}")
    
    subprocess.run(['cp', local_full_path, backup_full_path], check=True)
    print(f"Video file copied to backup: {backup_full_path}")
    
    play_video(local_full_path, loop_count)                                                 # Play the file using MPV, loop it loop_count times

    prev_update_time = curr_update_time                                                     # Update the previous update time to the current update time
    time.sleep(10)                                                                          # Wait for 10 seconds before the next check
  
  else:
    time.sleep(5)                                                                           # Wait for 5 seconds before the next check if the file hasn't been updated
