# AI_Light
This is AI Light project that was successfully demonstrated in Venice city, during the Venice glass week. 

In this version of the code, We need to setup the hardware such that everything is connected, and Arduino has the correct running code on it. 

-Use the Arduino software to upload "venice.ino" to the arduino for the firmware to run.

-Make sure that "runpod_watchdog.py" is added to the container. It should be under "/workspace/Open-Sora". During the project, we have to manually modified the aspect ratio of the display, since we didn't change the container code. 

-The two script to run on local computer is "venice.py" and "video_to_local.py". "venice.py" will also trigger "sound.py" and "voice_recognition.py" They are local library script that was refactored. There will also be some other library needed, but by running the above two scripts, the terminal will show you the missing library. 