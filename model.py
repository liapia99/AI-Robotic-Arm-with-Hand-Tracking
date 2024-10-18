import cv2
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model('gesture_recognition_model.h5')

# Box dimensions and position for capturing hand gestures
box_size = 300
box_x, box_y = 200, 200

# Capture from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip and draw the box
    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame, (box_x, box_y), (box_x + box_size, box_y + box_size), (0, 255, 0), 2)
    
    # Extract the region of interest (ROI) for prediction
    roi = frame[box_y:box_y + box_size, box_x:box_x + box_size]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    resized_roi = cv2.resize(gray_roi, (28, 28))
    normalized_roi = resized_roi / 255.0
    reshaped_roi = np.expand_dims(normalized_roi, axis=(0, -1))  # Reshape for model input
    
    # Predict the gesture
    predictions = model.predict(reshaped_roi)
    predicted_label = chr(np.argmax(predictions) + ord('A'))
    
    # Display the predicted gesture on the frame
    cv2.putText(frame, f'Predicted: {predicted_label}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    # Show the frame
    cv2.imshow('Hand Gesture Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q'
        break

cap.release()
cv2.destroyAllWindows()
