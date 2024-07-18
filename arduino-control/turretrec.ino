#include <Servo.h>
String inputString;

Servo left_right;
Servo up_down;

unsigned long lastSerialTime = 0;
const unsigned long timeout = 5000;

void setup() {
  // put your setup code here, to run once
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  left_right.attach(11);
  up_down.attach(10);
  Serial.begin(57600);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()){
    delay(100);
    lastSerialTime = millis();
    digitalWrite(13, LOW);
    inputString = Serial.readStringUntil('\r');
    Serial.println(inputString);
    int x = inputString.substring(0, inputString.indexOf(',')).toInt();
    int y = inputString.substring(inputString.indexOf(',') + 1).toInt();

    int theta_x = map(x, 0, 1920, 58, 132);
    int theta_y = map(y, 0, 1080, 113, 81);

    left_right.write(theta_x);
    up_down.write(theta_y);
  }

  if (millis() - lastSerialTime > timeout) {
    digitalWrite(13, HIGH);
  } else {
    digitalWrite(13, LOW);
  }
}
