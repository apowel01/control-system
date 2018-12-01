// Controlling Motors taking input from I2C to determine motor state
// Luke Leonard
// Nov 8 2018
// UPDATED: Dec 1 2018

#include <Wire.h>

#define SLAVE_ADDRESS 0x04

#define PWM_LOW_DELAY 20000
#define PWM_HIGH_ON_DELAY 1700
#define PWM_HIGH_OFF_DELAY 1500
#define PWM_HIGH_CRAWL_DELAY 999999999 // CHANGE LATER

int motorPin = 9;

enum {OFF, ON, CRAWL};
int motorState = OFF;

void setup() 
{
  Serial.begin(9600); // Setup serial console
  pinMode(motorPin, OUTPUT); // Set the motor pin
  
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receive_data);
  Wire.onRequest(send_data);
}
void loop() 
{
  switch(motorState)
  {
    case OFF:
      out_motor_low();
    break;
    
    case ON:
      out_motor_high();
    break;

    case CRAWL:
      
    break;
    
    default:
      digitalWrite(motorPin, LOW); // Default to off
    break;
  }
}

void out_motor_low() // PWM for the motor being off
{
  digitalWrite(motorPin, HIGH);
  delayMicroseconds(PWM_HIGH_OFF_DELAY);
  digitalWrite(motorPin, LOW);
  delayMicroseconds(PWM_LOW_DELAY);
 }

void out_motor_high() // PWM for the motor being on 
{
  digitalWrite(motorPin, HIGH);
  delayMicroseconds(PWM_HIGH_ON_DELAY);
  digitalWrite(motorPin, LOW);
  delayMicroseconds(PWM_LOW_DELAY);
}

void out_motor_crawl() // PWM for the motor going slowly (pod crawling)
{
  digitalWrite(motorPin, HIGH);
  delayMicroseconds(PWM_HIGH_CRAWL_DELAY);
  digitalWrite(motorPin, LOW);
  delayMicroseconds(PWM_LOW_DELAY);
}

void receive_data(int byteCount) // Function that gets called when the master sends any data
{
  if (Wire.available())
  {
    int num = Wire.read();
    switch (num)
    {
      case 0:
        motorState = OFF;
      break;

      case 1:
        motorState = ON;
      break;

      case 2:
        motorState = CRAWL;
      break;

      default:
        motorState = OFF;
      break;
    }
  }
}

void send_data() // Function that gets called when the master requests data
{
}
