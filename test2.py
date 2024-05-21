import cv2
import numpy as np

# Load the video
video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Function to calculate mean RGB values
def calculate_mean_rgb(frame):
    mean_rgb = cv2.mean(frame)[:3]  # Ignore the alpha channel if present
    return mean_rgb

# Desired frame rate (frames per second)
desired_fps = 1
delay = int(1000 / desired_fps)  # Delay in milliseconds

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break

    # Calculate the mean RGB values for the frame
    mean_rgb = calculate_mean_rgb(frame)
    
    # Display the mean RGB values on the frame
    mean_text = f"Mean RGB: ({mean_rgb[2]:.2f}, {mean_rgb[1]:.2f}, {mean_rgb[0]:.2f})"
    cv2.putText(frame, mean_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Show the frame
    cv2.imshow('Video', frame)
    
    # Wait for a specified delay and break the loop on 'q' key press
    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

# Release the video capture object and close display window
cap.release()
cv2.destroyAllWindows()