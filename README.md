# AI_Light
this is the main repository for project AI_Light for module E8004 at Aalto University

There are two main scripts: AI.py and light.py. AI.py is run to wait for customer press the button on the skull, then they can speak to the microphone. AI.py will generate a prompt based on the sound captured from the user. 

light.py will take the video and image downloaded from triton, and generate a suitable color scheme for arduino to display. It also play back the video. 

DigitalReadSerial.ino is a firmware that is flashed into arduino. This allow user interaction with button, and control the LED lighting accordingly. 

For installation, all the necessary can be installed using pip -install. Refer to error message for specific dependencies installation. We would consider a dependency list in future revision of the project 

Known bugs that should be fixed in future revision:
- sound capturing using microphone is buggy, as there can be multiple input to the PC. The python script should handle exception case better.
- LED light communication is lossy and often display inaccurate color.
- Automation with Triton is not completed.
  
