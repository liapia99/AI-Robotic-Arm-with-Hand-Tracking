# This code is meant to test communicating with Python code WITHOUT the web camera. Since this is my first time sending input values from Python to the serial monitor of Arduino IDE, I wanted to see if I could get the two to communicate first. 
# This code is used with talk_test.ino

import serial
import time

arduino_port = '/dev/cu.usbmodem2101' 
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

def move_servos(input_string):
    ser.write((input_string + '\n').encode())
    time.sleep(2)  # Arduino needs time to process data

if __name__ == "__main__":
    while True:
        input_value = input("Enter the servo positions (e.g., 00000 or 11111): ")
        move_servos(input_value)
