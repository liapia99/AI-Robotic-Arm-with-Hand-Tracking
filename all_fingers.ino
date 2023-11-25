#include <Servo.h>

Servo servoThumb;
Servo servoPointer;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

void setup() {
  servoThumb.attach(3);
  servoPointer.attach(5);
  servoMiddle.attach(6);
  servoRing.attach(9);
  servoPinky.attach(10);

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

    servoThumb.write(pos1);
    servoPointer.write(pos2);
    servoMiddle.write(pos3);
    servoRing.write(pos4);
    servoPinky.write(pos5);
  }
}
