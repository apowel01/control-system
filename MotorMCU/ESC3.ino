// Controlling Motors using arduino
// Luke Leonard
// Jan 26 2019

// MOTOR/ESC NEEDS AT LEAST 26V TO DO ANYTHING
#include <Servo.h>
//Servo esc; Create the object to control the esc
int motorPin = 9;
//int buttonPin = 2;
int throttle = 1500;
void setup() 
{
  Serial.begin(9600);
  pinMode(motorPin, OUTPUT);
  //pinMode(buttonPin, INPUT);
}
void loop() 
{ 
  if (Serial.available())
  {
    throttle = Serial.readStringUntil("\n").toInt();
  }
  
  digitalWrite(9, HIGH);
  delayMicroseconds(throttle);
  digitalWrite(9, LOW);
  delayMicroseconds(20000);
  Serial.println(throttle);
}
