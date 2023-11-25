# AI-Robotic-Arm-with-Hand-Tracking

Hi there! A couple months ago I rewatched Big Hero 6, a Disney movie about a group of friends with unique talents that form a superhero team to combat a masked villain threatening the city. Along with them is a healthcare provider robot named Baymax. I was inspired by Baymax to explored how engineering and healthcare can work together to get people the care they need. I found myself fascinated by the ongoing efforts to develop robots that assist healthcare professionals in diagnostics, surgeries, and patient care.

While I would love to make my own healthcare provider robot someday, I wanted to start with a feasible project for 2023. I began researching how I could build the differnt parts of Baymax. Step one, which is this project, is to build a robotic arm with artificial intelligence. Baymax is able to respond to its patients with appropriate gestures. Although this project does not program the arm to have responses to different gestures, it does use computer vision to track hand movements and replicate that on the 3D printed arm using **python**. 

Step two (2024): Build a dermatology image recognition system. This system will involve the use of computer vision and machine learning techniques to automatically identify and classify skin conditions based on images or scans. 


## IMPORTANT NOTES

Throughout the project, I encountered many issues. Here are the steps I recommend based on my troubleshooting:

- Start with finger_test.ino. From the servo, the brown wire goes to power, the orange/red goes to ground and the yellow goes to your digital pin. I used pins 3, 5, 6, 9, and 10. Test the "tendon" wiring of each servo by inputting 1 and 0 into the serial monitor. When the value is '1', the finger should open and when the value is '0', the finger should close towards the palm. Sometimes the servos do the opposite. Simply change the value of the write if this is the case.

- Here are the Python packages I installed:
   ``` pip install pyserial
       pip install mediapipe
       pip install serialDevice
       pip cvzone
   ```
