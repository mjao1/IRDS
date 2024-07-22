#include <Servo.h>
String inputString;

Servo left_right;
Servo up_down;

unsigned long lastSerialTime = 0; // Variable to store last serial data time
const unsigned long timeout = 5000; // Variable to store timeout duration to 5 seconds

void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  left_right.attach(11);
  up_down.attach(10);
  Serial.begin(57600);
}

void loop() {
  while(Serial.available()){
    lastSerialTime = millis(); // Update last serial time
    digitalWrite(13, LOW);
    inputString = Serial.readStringUntil('\r'); // Read incoming data from facerec.py until carriage return
    Serial.println(inputString);

    // Extract x and y coordinates from recieved string
    float x = inputString.substring(0, inputString.indexOf(',')).toInt();
    float y = inputString.substring(inputString.indexOf(',') + 1).toInt();

    // Map x and y coordinates from revieved string into external webcam FOV
    float theta_x = map(x, 0, 1920, 53, 128);
    float theta_y = map(y, 0, 1080, 110, 74);
    
    // Write mapped angles to each servos
    left_right.write(theta_x);
    up_down.write(theta_y);
  }

  // Check if no data has been received past timeout period and turn off laser diode if so
  if (millis() - lastSerialTime > timeout) {
    digitalWrite(13, HIGH);
  } else {
    digitalWrite(13, LOW);
  }
}
