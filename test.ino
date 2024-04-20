#include "LiquidCrystal_I2C.h"
#include <Wire.h>

int red_led = 13;
int green_led = 8;
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
   lcd.init();
   lcd.backlight();
   pinMode(red_led, OUTPUT);
   pinMode(green_led, OUTPUT);
   Serial.begin(9600);
   Serial.println("Waiting for distance from Serial Monitor...");
}

void loop() {
  while (!Serial.available());  // Wait until data is available
  delay(100);  // Delay to allow all serial data to arrive
  String input = Serial.readStringUntil('\n');  // Read input from Serial Monitor
  float distance = input.toFloat();  // Convert the input string to a float

  updateDisplay(distance);  // Update LED and LCD display
}

void updateDisplay(float distance) {
  if (distance > 12) {
    digitalWrite(red_led, LOW);  // Turn off red LED
    digitalWrite(green_led, HIGH);  // Turn on green LED
  } else {
    digitalWrite(green_led, LOW);  // Turn off green LED
    digitalWrite(red_led, HIGH);  // Turn on red LED
  }

  lcd.clear();  // Clear the LCD
  lcd.setCursor(0, 0);
  lcd.print("Object Detected at:");
  lcd.setCursor(0, 1);
  lcd.print(distance);
  delay(1000);
}
