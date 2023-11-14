#include <Servo.h>
#define numOfValsRec 5
#define digitsPerValRec 1

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

int valsRec[numOfValsRec];
//$00000
int stringLength = numOfValsRec * digitsPerValRec + 1;
int counter = 0;
bool counterStart = false;
String receivedString;


void setup() {
  // put your setup code here, to run once:
  Serial. begin(9600);
  servoThumb.attach(7);
  servoIndex.attach(7);
  servoMiddle.attach(7);
  servoRing.attach(7);
  servoPinky.attach(7);


}
void receiveData(){
  while (Serial.available()){
    char c = Serial.read();
    if (c=='$'){
      counterStart = true;
    }
    if (counterStart){
      if (counter < stringLength){
        receivedString = String(receivedString+c);
        counter++;
      }
      if (counter>=stringLength){
        for(int i = 0; i<numOfValsRec; i++){
          int num = (i*digitsPerValRec)+1;
        valsRec[i] = receivedString.substring(num, num + digitsPerValRec).toInt();
      }
      receivedString = "";
      counter = 0;
      counterStart = false;
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
