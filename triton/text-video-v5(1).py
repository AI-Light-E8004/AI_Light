import os
import torch
from diffusers import TextToVideoZeroPipeline
import numpy as np
import imageio

model_id = "runwayml/stable-diffusion-v1-5"
pipe = TextToVideoZeroPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
video_length = 12  # 24 ÷ 4fps = 6 seconds
chunk_size = 8

# Read prompt from file
with open("./outputText/text.txt", "r") as file:
    prompt = file.read().strip()

#prompt = "fantasy fish swimming"

seed = torch.seed()  # Get a new random seed

# Create folder to save images if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# Generate the video chunk-by-chunk, considering previous images
previous_images = None  # Initialize to track previous images
frame_ids = []  # Initialize list to hold frame ids for the entire video

# Generate frame ids for the entire video
for i in range(video_length):
    frame_ids.append(i)

# Split frame ids into chunks of size `chunk_size`
chunk_ids = [frame_ids[i:i + chunk_size] for i in range(0, len(frame_ids), chunk_size - 1)]

# Modify seed every 10 frames
change_seed_interval = 5

for i, chunk_frames in enumerate(chunk_ids):
    print(f"Processing chunk {i + 1} / {len(chunk_ids)}")
    
    # Generate a new random seed every 10 frames
    if i % change_seed_interval == 0 and i != 0:  # Change seed every 10 frames, starting from the second chunk
        seed = torch.seed()
        
    # Create a generator with the current seed
    generator = torch.Generator(device="cuda").manual_seed(seed)
    
    # Attach the first frame and previous chunk's last frame for Cross Frame Attention
    frame_ids = ([0] + chunk_frames[1:])  # Always include first frame and current chunk frames
    output = pipe(prompt=prompt, video_length=len(frame_ids), generator=generator, frame_ids=frame_ids)
    frames = output.images[1:]  # Discard first frame (already included in next chunk)

    # Save frames as JPG files
    for j, frame in enumerate(frames):
        imageio.imwrite(f"images/frame_{i * (chunk_size - 1) + j}.jpg", (frame * 255).astype("uint8"))

    # Update previous_images for the next chunk
    previous_images = output.images[-chunk_size + 1:]
