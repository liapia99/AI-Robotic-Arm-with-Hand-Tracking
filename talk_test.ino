// This code is meant to test communicating with Python code WITHOUT the web camera. Since this is my first time sending input values from Python to the serial monitor of Arduino IDE, I wanted to get the two to communicate first. 
// This code is used with talk_test.py 

#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

void setup() {
  servo1.attach(3);
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(9);
  servo5.attach(10);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');
    moveServos(inputString);
  }
}

void moveServos(String input) {
  if (input.length() == 5) {
    int pos1 = input.charAt(0) == '0' ? 0 : 180;
    int pos2 = input.charAt(1) == '0' ? 180 : 0;
    int pos3 = input.charAt(2) == '0' ? 180 : 0;
    int pos4 = input.charAt(3) == '0' ? 0 : 180;
    int pos5 = input.charAt(4) == '0' ? 0 : 180;

    servo1.write(pos1);
    servo2.write(pos2);
    servo3.write(pos3);
    servo4.write(pos4);
    servo5.write(pos5);
  }
}
