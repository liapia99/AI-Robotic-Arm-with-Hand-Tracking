# AI-Robotic-Arm-with-Hand-Tracking

For more in-depth documentation of the project: https://lukapia.notion.site/AI-Robotic-Arm-with-Hand-Tracking-170db8c15b69403f97ed5d3b6d776fba

Hi there! A few months ago, I rewatched Big Hero 6, a Disney movie about a group of friends with unique talents forming a superhero team to combat a masked villain threatening the city. Along with them is a healthcare provider robot named Baymax. Baymax inspired me to explore how engineering and healthcare can work together to get people the care they need. I was fascinated by the ongoing efforts to develop robots that assist healthcare professionals in diagnostics, surgeries, and patient care.

While I would love to make my own healthcare provider robot someday, I wanted to start with a feasible project for 2023. I began researching how I could build the different parts of Baymax. Step one, which is this project is to build a robotic arm with artificial intelligence. Baymax can respond to its patients with appropriate gestures. Although this project does not program the arm to have responses to different gestures, it does use computer vision to track hand movements and replicate that on the 3D printed arm using **python**. 

Step two (2024): Build a dermatology image recognition system. This system will automatically identify and classify skin conditions based on images or scans using computer vision and machine learning techniques. 


## Steps

- Start with finger_test.ino. From the servo, the brown wire goes to power, the orange/red goes to the ground, and the yellow goes to your digital pin. I used a mini breadboard to connect the ground and power for pins 3, 5, 6, 9, and 10. Test each servo's "tendon" wiring by inputting 1 and 0 into the serial monitor. When the value is '1', the finger should open, and when the value is '0', the finger should close towards the palm. Sometimes, the servos do the opposite. Simply change the value of the write if this is the case.

- Here are the Python packages I installed:
   ```
       pip install pyserial
       pip install mediapipe
       pip install serialDevice
       pip cvzone
   ```

- In the function `move_servos`, the fingers are determined to open or give the value '1' when the fingertip landmark is above the knuckle of that finger. I used the Mediapipe hand landmark model. 
<img width="1073" alt="hand-landmarks" src="https://github.com/liapia99/AI-Robotic-Arm-with-Hand-Tracking/assets/98356859/977a67f3-abdb-46c4-b090-85cb6d2fc756">

- In the `ser.write((command + '\n').encode('utf-8'))` line; it is **very** important to have the `'\n'` as the serial monitor in Arduino IDE will not know when the new command is given.

- **Make sure to CLOSE the Arduino IDE BEFORE running the Python code!** If you don't close the application, you will get error codes, and the webcam frame will not open properly.

- If you are still having trouble:
     - Press the restart button on your Arduino board and re-upload the Arduino code.
     - Try a different port on the computer, and make sure to note the change in your code.
     - Unplug the webcam and plug it back in. Sometimes, it does not register when you run the Python code.
     - If your fingers are not moving all the way up, make sure the string through the fingers is tight when in the position you want. If not,               tighten the wiring and even check if the pulley is fully screwed into the servo.
 
## Changes To Be Made

#Creating an OpenCV environment
- download Anaconda
- Open Linux terminal and write the following command: ```bash ~/Downloads/Anaconda3-2020.07-Linux-x86_64.sh```
- follow the directions to install Anaconda in the terminal
- https://saturncloud.io/blog/solving-the-conda-command-not-found-issue-after-installing-anaconda3/
- conda create -n opencv-env python=3.9.2 - version i have
- on linux debian
- Environments ensure that programs run consistently across machines by bundling up the packages and versions that the program was created with.
- 



- The thumb has a specific position to give the value '1'. So even when you have your thumb out like a thumbs-up gesture, the thumb is considered closed or given the value '0'. For now, in the code, I made the thumb give a value of '0' when the fingertip goes past the knuckle of the pointer finger. I also tried the palm's center and the pinky knuckle; however, these were hard to reach when doing a peace sign or a 🤟 gesture. 

