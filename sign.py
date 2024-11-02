import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe hands solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Initialize MediaPipe drawing solution
mp_drawing = mp.solutions.drawing_utils

def calculate_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def calculate_angle(a, b, c):
    ab = np.array(b) - np.array(a)
    bc = np.array(c) - np.array(b)
    cos_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(cos_angle))
    return angle

def analyze_hand_landmarks(landmarks, image_shape, wrist_depth):
    results = {'fingers': {}, 'wrist_tilt': 'center', 'wrist_rotation': 'center', 'wrist_tilt_angle': 0, 'wrist_rotation_angle': 0}
    # (Omitted: code analyzing the hand and setting the results dictionary.)
    return results

def detect_sign_language_letter(analysis):
 """
    This function takes the hand analysis results and maps them to a sign language letter.
    """
    thumb_status = analysis['fingers']['thumb']['status']
    index_status = analysis['fingers']['index']['status']
    middle_status = analysis['fingers']['middle']['status']
    ring_status = analysis['fingers']['ring']['status']
    pinky_status = analysis['fingers']['pinky']['status']

    # Letter 'A': All fingers closed except thumb
    if (thumb_status == 'closed' and
        index_status == 'closed' and
        middle_status == 'closed' and
        ring_status == 'closed' and
        pinky_status == 'closed'):
        return 'A'

    # Letter 'B': All fingers open, thumb across palm
    elif (thumb_status == 'closed' and
          index_status == 'open' and
          middle_status == 'open' and
          ring_status == 'open' and
          pinky_status == 'open'):
        return 'B'

    # Letter 'C': All fingers curved as if holding a cup
    elif (thumb_status == 'curved' and
          index_status == 'curved' and
          middle_status == 'curved' and
          ring_status == 'curved' and
          pinky_status == 'curved'):
        return 'C'

    # Letter 'D': Index finger up, other fingers in a fist, thumb touching middle finger
    elif (thumb_status == 'touching_middle' and
          index_status == 'open' and
          middle_status == 'closed' and
          ring_status == 'closed' and
          pinky_status == 'closed'):
        return 'D'

    # Letter 'E': All fingers curled toward palm, thumb crossing over
    elif (thumb_status == 'crossing' and
          index_status == 'curved' and
          middle_status == 'curved' and
          ring_status == 'curved' and
          pinky_status == 'curved'):
        return 'E'

    # Letter 'F': Thumb and index finger form a circle, other fingers extended
    elif (thumb_status == 'touching_index' and
          index_status == 'touching_thumb' and
          middle_status == 'open' and
          ring_status == 'open' and
          pinky_status == 'open'):
        return 'F'

    # Letter 'G': Thumb and index finger extended, other fingers closed
    elif (thumb_status == 'closed' and
          index_status == 'open' and
          middle_status == 'closed' and
          ring_status == 'closed' and
          pinky_status == 'closed'):
        return 'G'

    # Letter 'H': Index and middle fingers extended, other fingers closed
    elif (thumb_status == 'closed' and
          index_status == 'open' and
          middle_status == 'open' and
          ring_status == 'closed' and
          pinky_status == 'closed'):
        return 'H'

    # Letter 'I': Pinky finger extended, other fingers closed
    elif (thumb_status == 'closed' and
          index_status == 'closed' and
          middle_status == 'closed' and
          ring_status == 'closed' and
          pinky_status == 'open'):
        return 'I'

    # No letter detected
    return None


# OpenCV video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    result = hands.process(image_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on image
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                      landmark_drawing_spec=mp_drawing.DrawingSpec(color=(120, 81, 169), thickness=2, circle_radius=4))

            # Analyze landmarks
            analysis = analyze_hand_landmarks(hand_landmarks.landmark, image.shape, wrist_depth=10)  # Depth in inches

            # Detect the sign language letter
            detected_letter = detect_sign_language_letter(analysis)
            
            if detected_letter:
                # Display the detected letter on the screen
                cv2.putText(image, f"Letter: {detected_letter}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

    # Display the image
    cv2.imshow('Hand Tracking', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
