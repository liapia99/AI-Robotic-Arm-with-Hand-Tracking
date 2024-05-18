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

def analyze_hand_landmarks(landmarks, image_shape, wrist_depth):
    results = {'fingers': {}, 'wrist_tilt': 'center', 'wrist_tilt_angle': 0}

    # Get coordinates of landmarks
    coords = [(int(landmark.x * image_shape[1]), int(landmark.y * image_shape[0]), landmark.z) for landmark in landmarks]

    # Calculate distance from camera using wrist (Landmark 0)
    wrist = coords[0]
    nose_tip = [int(image_shape[1] / 2), int(image_shape[0] / 2)]  # Approx. center of the image
    distance_in_pixels = calculate_distance(wrist[:2], nose_tip)
    # Convert distance from pixels to inches using a constant depth of the wrist from the camera
    distance_in_inches = wrist_depth * (distance_in_pixels / image_shape[1])  
    results['distance_from_camera'] = distance_in_inches

    # Get the average depth of landmarks 5, 9, 13, 17
    finger_mcp_indices = [5, 9, 13, 17]
    average_finger_depth = np.mean([coords[i][2] for i in finger_mcp_indices])
    wrist_depth = wrist[2]

    # Check wrist tilt based on depth and calculate the tilt angle
    depth_difference = wrist_depth - average_finger_depth
    tilt_angle = np.interp(depth_difference, [-0.1, 0.1], [-30, 80])  # Map depth difference to angle
    tilt_angle = round(tilt_angle)

    if tilt_angle < 10:
        results['wrist_tilt'] = 'back'
    elif tilt_angle > 55:
        results['wrist_tilt'] = 'forward'
    else:
        results['wrist_tilt'] = 'center'
        
    results['wrist_tilt_angle'] = tilt_angle

    # Thumb (Landmarks: 1-4)
    thumb_tip = coords[4]
    thumb_mcp = coords[1]
    thumb_ip = coords[3]

    if thumb_tip[0] < thumb_mcp[0]:  # Thumb is open
        results['fingers']['thumb'] = 'open'
    else:
        results['fingers']['thumb'] = 'closed'

    # Other fingers (Landmarks: 5-20, with 4 landmarks per finger)
    finger_tips = [8, 12, 16, 20]
    finger_mcp = [5, 9, 13, 17]

    for i, tip in enumerate(finger_tips):
        finger_name = ['index', 'middle', 'ring', 'pinky'][i]
        if coords[tip][1] < coords[finger_mcp[i]][1]:  # Finger is open
            results['fingers'][finger_name] = 'open'
        else:
            results['fingers'][finger_name] = 'closed'

    return results

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
            print(analysis)

            # Draw circles indicating the depth of each landmark
            for i, landmark in enumerate(hand_landmarks.landmark):
                x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
                depth_color = (0, 0, 0)  # Default color for non-wrist landmarks

                if i == 0:  # Wrist landmark
                    if analysis['wrist_tilt'] == 'back':
                        depth_color = (0, 0, 0)  # Black for back tilt
                    elif analysis['wrist_tilt'] == 'forward':
                        depth_color = (255, 255, 255)  # White for forward tilt
                    else:
                        depth_color = (128, 128, 128)  # Gray for center tilt
                else:  # Finger tip landmarks
                    if analysis['wrist_tilt'] == 'back':
                        depth_color = (255, 255, 255)  # White for back tilt
                    elif analysis['wrist_tilt'] == 'forward':
                        depth_color = (0, 0, 0)  # Black for forward tilt
                    else:
                        depth_color = (128, 128, 128)  # Gray for center tilt

                cv2.circle(image, (x, y), 5, depth_color, -1)

    # Display the image
    cv2.imshow('Hand Tracking', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
