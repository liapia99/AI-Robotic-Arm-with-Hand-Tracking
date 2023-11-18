import cv2
import mediapipe as mp
import serial
import time

# Make sure to install the following packages: cvzone, mediapipe

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# OpenCV setup
cap = cv2.VideoCapture(0)  # Use 0 for the default camera
mySerial = serial.Serial("COM3", 256000)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with mediapipe hands
    results = hands.process(rgb_frame)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:

            # Send data to the serial monitor
            hand_data = []
            for idx, point in enumerate(landmarks.landmark):
                x, y, z = point.x, point.y, point.z  # Get x, y, z coordinates of the landmark
                hand_data.append(f"{x},{y},{z}")

            data_to_send = "$" + "".join(hand_data)  # Add "$" at the beginning
            mySerial.write(data_to_send.encode())
            mySerial.flush()

            # Adding a delay to help the serial monitor process the data collected
            time.sleep(0.1)

            # Draw lines through the fingers
            finger_connections = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (0, 9), (9, 10),
                                  (10, 11), (11, 12), (0, 13), (13, 14), (14, 15), (15, 16), (0, 17), (17, 18),
                                  (18, 19), (19, 20)]
            for connection in finger_connections:
                x1, y1 = int(landmarks.landmark[connection[0]].x * frame.shape[1]), int(
                    landmarks.landmark[connection[0]].y * frame.shape[0])
                x2, y2 = int(landmarks.landmark[connection[1]].x * frame.shape[1]), int(
                    landmarks.landmark[connection[1]].y * frame.shape[0])
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Break the loop if 'x' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
mySerial.close()
