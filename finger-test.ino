#include <Servo.h>

Servo servoRing;  // Define ring finger servo
int receivedValue = 0;  // Variable to store received data

void setup() {
  Serial.begin(9600);
  servoRing.attach(3);  // Set ring finger servo to digital pin 3
}

void loop() {
  if (Serial.available() > 0) {
    receivedValue = Serial.read() - '0';  // Read the received data and convert ASCII to integer
    moveServo(receivedValue);  // Move the servo based on the received data
  }
}

void moveServo(int value) {
  if (value == 0) {
    // Move to max position when '0' is received
    servoRing.write(180);
  } else if (value == 1) {
    // Move back to original position when '1' is received
    servoRing.write(0);  // Adjust the value to the original position
  }
}
