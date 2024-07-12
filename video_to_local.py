import paramiko
import time
import subprocess
import os
from scp import SCPClient

# Remote server details
username = 'root'    
ip = '127.0.0.1'                 # <-- ADD IP-ADDRESS OF REMOTE HOST
port = 22                        # <-- ADD PORT OF REMOTE HOST
key_path = '~/.ssh/id_ed25519'   # path to private ssh ed25519 key

# Paths to correct folders
remote_file_path = '/workspace/Open-Sora/samples/samples/sample_0000.mp4'         # Output file of the AI model
local_file_path = '/aiproject/output_samples/'                                    # Destination file path where video is stored on local for playback
backup_folder_path = '/aiproject/backup_samples'                                  # Destination file path where every output is stored

# Define loop count for video playback
loop_count = 7

# FUNCTION1: Establish an SSH connection to the remote server.
def ssh_client(username, ip, port, key_path):
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(username, ip, port, key_filename=key_path)
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

# FUNCTION5: Play the video file using VLC, looping it the specified number of times.
def play_video(file_path, loop_count):
    for _ in range(loop_count):
        subprocess.run(['vlc', '--play-and-exit', file_path])


# Establish SSH client connection
client = ssh_client(username, ip, port, key_path)

# Initial modification time of the file
prev_update_time = get_update_time(client, remote_file_path)

while True:
  curr_update_time = get_update_time(client, remote_file_path)
  
  if curr_update_time != prev_update_time:
    
    local_full_path = os.path.join(local_file_path, os.path.basename(remote_file_path))     # Construct the full local path for the file
    file_transfer(client, remote_file_path, local_full_path)                                # Transfer the file from the remote server to the local path

    next_backup_filename = get_next_filename(backup_folder_path, 'sample_', '.mp4')         # Generate the next backup filename with a running number
    backup_full_path = os.path.join(backup_folder_path, next_backup_filename)
    
    os.rename(local_full_path, backup_full_path)                                            # Move the transferred file to the backup folder with the new name
    os.rename(backup_full_path, local_full_path)                                            # Move the file back to the local folder with the original name
        
    play_video(local_full_path, loop_count)                                                 # Play the file using VLC, loop it loop_count times

    prev_update_time = curr_update_time                                                     # Update the previous update time to the current update time
    time.sleep(10)                                                                          # Wait for 10 seconds before the next check
  
  else:
    time.sleep(5)                                                                           # Wait for 5 seconds before the next check if the file hasn't been updated
