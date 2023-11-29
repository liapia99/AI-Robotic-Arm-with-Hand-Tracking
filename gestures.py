import cv2
import mediapipe as mp
import serial


arduino_port = "/dev/cu.usbmodem2101"  # Change this to your Arduino port
arduino_baudrate = 9600
ser = serial.Serial(arduino_port, arduino_baudrate, timeout=1)

# Setting up Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1) # Only recognizes one hand

# Initialize the webcam
cap = cv2.VideoCapture(0)

def move_servos(hand_landmarks):
    # Marking the fingertip points
    thumb_tip_y = hand_landmarks.landmark[4].y
    pointer_tip_y = hand_landmarks.landmark[8].y
    middle_tip_y = hand_landmarks.landmark[12].y
    ring_tip_y = hand_landmarks.landmark[16].y
    pinky_tip_y = hand_landmarks.landmark[20].y
    
    # If the fingertips go past these points, then the fingers are closed
    thumb_knuckle_y = hand_landmarks.landmark[5].y
    pointer_knuckle_y = hand_landmarks.landmark[5].y
    middle_knuckle_y = hand_landmarks.landmark[9].y
    ring_knuckle_y = hand_landmarks.landmark[13].y
    pinky_knuckle_y = hand_landmarks.landmark[17].y

    thumb_closed = 1 if thumb_tip_y < thumb_knuckle_y else 0
    pointer_closed = 1 if pointer_tip_y < pointer_knuckle_y else 0
    middle_closed = 1 if middle_tip_y < middle_knuckle_y else 0
    ring_closed = 1 if ring_tip_y < ring_knuckle_y else 0
    pinky_closed = 1 if pinky_tip_y < pinky_knuckle_y else 0

    # Determine if the middle finger is given
    middlefinger1 = thumb_tip_y < thumb_knuckle_y and pointer_tip_y < pointer_knuckle_y
    middlefinger2 = middle_tip_y < middle_knuckle_y and ring_tip_y < ring_knuckle_y and pinky_tip_y < pinky_knuckle_y

    # If so, make the hand open 
    thumb_closed = 1 if middlefinger1 else 0
    pointer_closed = 1 if middlefinger1 else 0
    middle_closed = 1 if middlefinger2 else 0
    ring_closed = 1 if middlefinger2 else 0
    pinky_closed = 1 if middlefinger2 else 0

    command = f"{thumb_closed}{pointer_closed}{middle_closed}{ring_closed}{pinky_closed}"
    print(f"Sending command: {command}")
    ser.write((command + '\n').encode('utf-8'))

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Display the webcam frame
    cv2.imshow("Hand Tracking", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press 'q' to exit the loop
    if key == ord('q'):
        break

    # Convert frame to RGB for MediaPipe Hands processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # Check if a hand is detected
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Take the first detected hand
        move_servos(hand_landmarks)


# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()
