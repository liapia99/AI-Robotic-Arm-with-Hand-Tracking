from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
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

    # Get coordinates of landmarks
    coords = [(int(landmark.x * image_shape[1]), int(landmark.y * image_shape[0]), landmark.z) for landmark in landmarks]

    # Calculate distance from camera using wrist (Landmark 0)
    wrist = coords[0]
    nose_tip = [int(image_shape[1] / 2), int(image_shape[0] / 2)]  # Approx. center of the image
    distance_in_pixels = calculate_distance(wrist[:2], nose_tip)
    # Convert distance from pixels to inches using a constant depth of the wrist from the camera
    distance_in_inches = wrist_depth * (distance_in_pixels / image_shape[1])
    #results['distance_from_camera'] = distance_in_inches

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

    # Check wrist rotation based on depth difference between landmarks 1 and 17
    landmark_1_depth = coords[1][2]
    landmark_17_depth = coords[17][2]

    depth_difference_rotation = landmark_1_depth - landmark_17_depth
    rotation_angle = np.interp(depth_difference_rotation, [-0.1, 0.1], [-90, 90])  # Map depth difference to angle
    rotation_angle = round(rotation_angle)

    if rotation_angle < -5:
        results['wrist_rotation'] = 'right'
    elif rotation_angle > 5:
        results['wrist_rotation'] = 'left'
    else:
        results['wrist_rotation'] = 'center'

    results['wrist_rotation_angle'] = rotation_angle

    # Thumb (Landmarks: 1-4)
    thumb_tip = coords[4]
    thumb_mcp = coords[1]
    thumb_ip = coords[3]

    if thumb_tip[0] < thumb_mcp[0]:  # Thumb is open
        results['fingers']['thumb'] = {'status': 'open'}
    else:
        results['fingers']['thumb'] = {'status': 'closed'}

    # Check thumb tilt
    thumb_depth_difference = thumb_tip[2] - thumb_ip[2]
    thumb_tilt_angle = np.interp(thumb_depth_difference, [-0.1, 0.1], [-90, 90])
    thumb_tilt_angle = round(thumb_tilt_angle)

    if thumb_tilt_angle < -10:
        results['fingers']['thumb']['tilt'] = 'right'
    elif thumb_tilt_angle > 10:
        results['fingers']['thumb']['tilt'] = 'left'
    else:
        results['fingers']['thumb']['tilt'] = 'center'

    # Index finger (Landmarks: 5-6-9)
    index_angles = (5, 6, 9)
    mcp, pip, adjacent_mcp = index_angles

    if coords[pip][1] < coords[mcp][1]:  # Finger is open
        results['fingers']['index'] = {'status': 'open'}
    else:
        results['fingers']['index'] = {'status': 'closed'}

    # Calculate the angle at the MCP joint for the index finger
    index_angle = calculate_angle(coords[adjacent_mcp], coords[mcp], coords[pip])
    
    if index_angle > 95:
        results['fingers']['index']['tilt'] = 'right'
    elif index_angle < 80:
        results['fingers']['index']['tilt'] = 'left'
    else:
        results['fingers']['index']['tilt'] = 'center'

    # Other fingers (Landmarks: 9-10-5, 13-14-9, 17-18-13)
    finger_angles = [
        (9, 10, 5),  # Middle
        (13, 14, 9), # Ring
        (17, 18, 13) # Pinky
    ]

    angle_thresholds = {
        'middle': (80, 90), # Adjusted to normal order for correct tilt
        'ring': (80, 90),
        'pinky': (80, 90)
    }

    for i, (mcp, pip, adjacent_mcp) in enumerate(finger_angles):
        finger_name = ['middle', 'ring', 'pinky'][i]
        if coords[pip][1] < coords[mcp][1]:  # Finger is open
            results['fingers'][finger_name] = {'status': 'open'}
        else:
            results['fingers'][finger_name] = {'status': 'closed'}

        # Calculate the angle at the MCP joint
        angle = calculate_angle(coords[adjacent_mcp], coords[mcp], coords[pip])
        
        lower_threshold, upper_threshold = angle_thresholds[finger_name]
        if angle > upper_threshold:
            results['fingers'][finger_name]['tilt'] = 'left'
        elif angle < lower_threshold:
            results['fingers'][finger_name]['tilt'] = 'right'
        else:
            results['fingers'][finger_name]['tilt'] = 'center'

    return results

def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            image = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result = hands.process(image_rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    analysis = analyze_hand_landmarks(hand_landmarks.landmark, image.shape, wrist_depth=10)
                    print(analysis)

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
