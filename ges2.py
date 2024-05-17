import cv2
import mediapipe as mp
import math

# Setting up Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # Only recognizes one hand
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
  
def calculate_distance(landmark1, landmark2):
    return math.sqrt((landmark1.x - landmark2.x) ** 2 + 
                     (landmark1.y - landmark2.y) ** 2 + 
                     (landmark1.z - landmark2.z) ** 2)
  
def move_servos(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]
    pointer_tip = hand_landmarks.landmark[8]
    pointer_pip = hand_landmarks.landmark[6]
    middle_tip = hand_landmarks.landmark[12]
    middle_pip = hand_landmarks.landmark[10]
    ring_tip = hand_landmarks.landmark[16]
    ring_pip = hand_landmarks.landmark[14]
    pinky_tip = hand_landmarks.landmark[20]
    pinky_pip = hand_landmarks.landmark[18]

    thumb_closed = 1 if calculate_distance(thumb_tip, thumb_ip) &lt; calculate_distance(hand_landmarks.landmark[2], thumb_ip) else 0
    pointer_closed = 1 if calculate_distance(pointer_tip, pointer_pip) &lt; calculate_distance(hand_landmarks.landmark[5], pointer_pip) else 0
    middle_closed = 1 if calculate_distance(middle_tip, middle_pip) &lt; calculate_distance(hand_landmarks.landmark[9], middle_pip) else 0
    ring_closed = 1 if calculate_distance(ring_tip, ring_pip) &lt; calculate_distance(hand_landmarks.landmark[13], ring_pip) else 0
    pinky_closed = 1 if calculate_distance(pinky_tip, pinky_pip) &lt; calculate_distance(hand_landmarks.landmark[17], pinky_pip) else 0

    # Set the corresponding fingers to be closed based on the conditions
    command = f"{thumb_closed}{pointer_closed}{middle_closed}{ring_closed}{pinky_closed}"

    # Check for specific binary sequences and replace them with '11111'
    if command == '10100' or command == '00100':
        command = '11111'

    print(f"Sending command: {command}")
    
def draw_landmarks_with_depth(image, hand_landmarks):
    for landmark in hand_landmarks.landmark:
        x = int(landmark.x * image.shape[1])
        y = int(landmark.y * image.shape[0])
        z = landmark.z

        # Normalize the z value to a 0-1 range
        z_normalized = (1 - z) * 255  # Inverse to make closer points brighter
        z_normalized = max(0, min(255, z_normalized))  # Clamp to 0-255

        # Draw the circle with the color intensity based on z value
        color = (int(z_normalized), int(z_normalized), int(z_normalized))
        cv2.circle(image, (x, y), 5, color, -1)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Check if frame is successfully captured
    if not ret:
        print("Webcam has crashed! Sending arm to position '11111'")
        break

    # Convert frame to RGB for MediaPipe Hands processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # Check if a hand is detected
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Take the first detected hand
        move_servos(hand_landmarks)
        draw_landmarks_with_depth(frame, hand_landmarks)

    # Display the frame with landmarks
    cv2.imshow("Hand Tracking", frame)

    key = cv2.waitKey(1) & 0xFF

    # Press 'q' to exit the loop
    if key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
