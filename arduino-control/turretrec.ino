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
    delay(100);
    lastSerialTime = millis(); // Update last serial time
    digitalWrite(13, LOW);
    inputString = Serial.readStringUntil('\r'); // Read incoming data from facerec.py until carriage return
    Serial.println(inputString);

    // Extract x and y coordinates from recieved string
    int x = inputString.substring(0, inputString.indexOf(',')).toInt();
    int y = inputString.substring(inputString.indexOf(',') + 1).toInt();

    // Map x and y coordinates from revieved string into external webcam FOV
    int theta_x = map(x, 0, 1920, 58, 132);
    int theta_y = map(y, 0, 1080, 113, 81);
    
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
