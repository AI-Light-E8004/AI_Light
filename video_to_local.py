import paramiko
import time
import subprocess
from scp import SCPClient

#Remote server details
username = 'root'    
ip = '127.0.0.1'                 # <-- ADD IP-ADDRESS OF REMOTE HOST
port = 22                        # <-- ADD PORT OF REMOTE HOST
key_path = '~/.ssh/id_ed25519'   # path to private ssh ed25519 key

# Paths to correct folders
remote_file_path = '/workspace/Open-Sora/samples/samples/sample_0000.mp4'   # Output file of the AI model
local_file_path = '/aiproject/output_samples/'                              # Destination file path where video is stored on local

def get_update_time(client, path):
  stdin, stdout, stderr = client.exec_command(f'stat -c %Y {path}' )

  update_time = stdout.read().strip()
  error_msg_poll = stderr.read().strip()

  if error_msg_poll:
    raise Exception(f"Error getting modification time: {error_msg_poll}")

  return int(update_time)



prev_update_time = get_update_time(client, remote_file_path)

while True:
  current_update_time = get_update_time(client, remote_file_path)
