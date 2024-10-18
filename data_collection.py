import cv2
import numpy as np
import os
import time

output_dir = 'captured_images'  
os.makedirs(output_dir, exist_ok=True)

# Box dimensions and position
box_size = 300
box_x, box_y = 200, 200  # Top-left corner of the box

def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            image = cv2.flip(frame, 1)

            # Draw the box on the frame
            cv2.rectangle(image, (box_x, box_y), (box_x + box_size, box_y + box_size), (0, 255, 0), 2)

            # Overlay instructions on the frame ( only from A to I ) 
            cv2.putText(image, 'Position your hand in the green box', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(image, 'Press "A" to "I" to capture images', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Capture images when a key is pressed
            key = cv2.waitKey(1)
            if key == ord('a'):  # If the user presses 'a'
                img_name = os.path.join(output_dir, 'A_{}.jpeg'.format(int(time.time())))
                cropped_image = image[box_y:box_y + box_size, box_x:box_x + box_size]
                cv2.imwrite(img_name, cropped_image)
                print(f"Image saved: {img_name}")
            elif key == ord('b'):  # If the user presses 'b'
                img_name = os.path.join(output_dir, 'B_{}.jpeg'.format(int(time.time())))
                cropped_image = image[box_y:box_y + box_size, box_x:box_x + box_size]
                cv2.imwrite(img_name, cropped_image)
                print(f"Image saved: {img_name}")
            elif key == ord('c'):  # If the user presses 'c'
                img_name = os.path.join(output_dir, 'C_{}.jpeg'.format(int(time.time())))
                cropped_image = image[box_y:box_y + box_size, box_x:box_x + box_size]
                cv2.imwrite(img_name, cropped_image)
                print(f"Image saved: {img_name}")
            elif key == ord('d'):  # If the user presses 'd'
                img_name = os.path.join(output_dir, 'D_{}.jpeg'.format(int(time.time())))
                cropped_image = image[box_y:box_y + box_size, box_x:box_x + box_size]
                cv2.imwrite(img_name, cropped_image)
                print(f"Image saved: {img_name}")
            elif key == ord('e'):  # If the user presses 'e'
                img_name = os.path.join(output_dir, 'E_{}.jpeg'.format(int(time.time())))
                cropped_image = image[box_y:box_y + box_size, box_x:box_x + box_size]
                cv2.imwrite(img_name, cropped_image)
                print(f"Image saved: {img_name}")
            elif key == ord('f'):  # If the user presses 'f'
                img_name = os.path.join(output_dir, 'F_{}.jpeg'.format(int(time.time())))
                cropped_image = image[box_y:box_y + box_size, box_x:box_x + box_size]
                cv2.imwrite(img_name, cropped_image)
                print(f"Image saved: {img_name}")
            elif key == ord('g'):  # If the user presses 'g'
                img_name = os.path.join(output_dir, 'G_{}.jpeg'.format(int(time.time())))
                cropped_image = image[box_y:box_y + box_size, box_x:box_x + box_size]
                cv2.imwrite(img_name, cropped_image)
                print(f"Image saved: {img_name}")
            elif key == ord('h'):  # If the user presses 'h'
                img_name = os.path.join(output_dir, 'H_{}.jpeg'.format(int(time.time())))
                cropped_image = image[box_y:box_y + box_size, box_x:box_x + box_size]
                cv2.imwrite(img_name, cropped_image)
                print(f"Image saved: {img_name}")
            elif key == ord('i'):  # If the user presses 'i'
                img_name = os.path.join(output_dir, 'I_{}.jpeg'.format(int(time.time())))
                cropped_image = image[box_y:box_y + box_size, box_x:box_x + box_size]
                cv2.imwrite(img_name, cropped_image)
                print(f"Image saved: {img_name}")

            # Display the frame
            cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key
            break

    cap.release()
    cv2.destroyAllWindows()

gen_frames()
