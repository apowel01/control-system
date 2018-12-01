// Controlling Motors using button press on/off
// Luke Leonard
// Nov 8 2018
// UPDATED: Dec 1 2018

int motorPin = 9;
int buttonPin = 2;

enum {OFF, ON};
int motorState = OFF;

const int PWM_LOW_DELAY = 20000;
const int PWM_HIGH_ON_DELAY = 1700;
const int PWM_HIGH_OFF_DELAY = 1500;

void setup() 
{
  Serial.begin(9600); // Setup serial console
  pinMode(motorPin, OUTPUT); // Set the motor pin
  pinMode(buttonPin, INPUT); // Set the button pin
}
void loop() 
{
  // Every button press change the state of the motor
  if (digitalRead(buttonPin) == HIGH)
  {
    Serial.println("State 1: MOtor running");
    motorState = ON; // Motor running (Not sure speed right now)
  }
  else
  {
    Serial.println("State 0: Motor off");
    motorState = OFF; // Motor not running
  }

  switch(motorState)
  {
    case OFF:
      out_motor_low();
    break;
    
    case ON:
      out_motor_high();
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
