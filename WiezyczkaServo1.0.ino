#include <cvzone.h>
#include <Servo.h>

SerialData serialData(1, 1);
int valsRec[1];

Servo myServo;
const int servoPin = 6;

void setup() {
  Serial.begin(115200);
  serialData.begin();
  
  myServo.attach(servoPin);
  
  
  myServo.writeMicroseconds(1500);  
  delay(1000);  
}

void moveServoSlowly(int targetMicroseconds) {
  myServo.writeMicroseconds(targetMicroseconds);  
  delay(100);  
}

void loop() {
  serialData.Get(valsRec);
  int command = valsRec[0];

  Serial.print("Otrzymana komenda: ");
  Serial.println(command);

  if (command == 2) {  // Ruch w prawo (zgodnie ze wskazówkami zegara)
    moveServoSlowly(1475.5);  )
  } 
  else if (command == 3) {  // Ruch w lewo (przeciwnie do wskazówek zegara)
    moveServoSlowly(1542);  
  } 
  else {  // command == 1 (STOP) 
    moveServoSlowly(1500);  // STOP 
  }

  delay(20);  
}
