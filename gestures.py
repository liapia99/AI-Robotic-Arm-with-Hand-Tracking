import cv2
import mediapipe as mp

# Set up mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # Set max_num_hands to 1

cap = cv2.VideoCapture(0)
class SerialObject:
    def __init__(self, port, baud, digits):
        self.port = port
        self.baud = baud
        self.digits = digits

    def sendData(self, myString):
        try:
            # Check if the string starts with '$' and exclude it
            if myString.startswith('$'):
                myString = myString[1:]
            # Extract the numeric part of the string and convert it to an integer
            numeric_part = int(''.join(c if c.isdigit() or c == '.' else ' ' for c in myString).split()[0])
            # Convert the numeric part to a string and fill with leading zeros
            myString = str(numeric_part).zfill(self.digits)
            # Add the "$" character at the beginning
            myString = "$" + myString
            print(f"Sending: {myString}")  # For debugging
        except Exception as e:
            print(f"Error in sendData: {e}")


# Now create an instance of SerialObject
mySerial = SerialObject("/dev/cu.usbmodem8401", 250000, 5) 

while True:
    success, img = cap.read()
    if not success:
        break

    # Convert BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Process the frame with mediapipe hands
    results = hands.process(img_rgb)
    # Check if a hand is detected
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # Take the first detected hand

        # Get the y-coordinates of the tip landmarks of each finger
        thumb_tip_y = hand_landmarks.landmark[4].y
        pointer_tip_y = hand_landmarks.landmark[8].y
        middle_tip_y = hand_landmarks.landmark[12].y
        ring_tip_y = hand_landmarks.landmark[16].y
        pinky_tip_y = hand_landmarks.landmark[20].y

        # Get the y-coordinates of the knuckle landmarks of each finger
        thumb_knuckle_y = hand_landmarks.landmark[5].y
        pointer_knuckle_y = hand_landmarks.landmark[5].y
        middle_knuckle_y = hand_landmarks.landmark[9].y
        ring_knuckle_y = hand_landmarks.landmark[13].y
        pinky_knuckle_y = hand_landmarks.landmark[17].y

        # Determine if the fingers are closed or open
        thumb_closed = 1 if thumb_tip_y < thumb_knuckle_y else 0
        pointer_closed = 1 if pointer_tip_y < pointer_knuckle_y else 0
        middle_closed = 1 if middle_tip_y < middle_knuckle_y else 0
        ring_closed = 1 if ring_tip_y < ring_knuckle_y else 0
        pinky_closed = 1 if pinky_tip_y < pinky_knuckle_y else 0

        connections = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 8), (9, 10),
                       (10, 11), (11, 12), (13, 14), (14, 15), (15, 16), (17, 18), (18, 19), (19, 20)]
        for connection in connections:
            x1, y1 = int(hand_landmarks.landmark[connection[0]].x * img.shape[1]), int(
                hand_landmarks.landmark[connection[0]].y * img.shape[0])
            x2, y2 = int(hand_landmarks.landmark[connection[1]].x * img.shape[1]), int(
                hand_landmarks.landmark[connection[1]].y * img.shape[0])
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue lines

        # Send data to serial
        data_to_send = f"{thumb_closed}{pointer_closed}{middle_closed}{ring_closed}{pinky_closed}"
        mySerial.sendData(data_to_send)

    # Display 
    cv2.imshow("Hand Tracking", img)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
