#include <Servo.h>

Servo servo1;  // Define servo
int receivedValue = 0;  // Variable to store received data

void setup() {
  Serial.begin(9600);
  servo1.attach(3);  // Set servo to digital pin 3 - can check all five servos by changing this value
}

void loop() {
  if (Serial.available() > 0) {
    receivedValue = Serial.read() - '0';  // Read the received data and convert ASCII to integer
    moveServo(receivedValue);  // Move the servo based on the received data
  }
}

void moveServo(int value) {
  if (value == 0) {
    // Move to "closed finger" position when '0' is received
    servo1.write(0);
  } else if (value == 1) {
    // Move to "open finger" position when '1' is received
    servo1.write(180);  
    // For some servos, it might be necessary to adjust the value that is written
  }
}
