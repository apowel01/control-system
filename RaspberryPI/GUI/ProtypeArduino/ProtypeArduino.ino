#include <math.h>
#include <stdint.h>
#include <Servo.h>
#include <Wire.h>
#include <Adafruit_ADS1015.h>
 
Adafruit_ADS1115 ads1115;  //ADC object
Servo motor;  //Motor Object
double disp_lastTime = 0;
double disp_sampleTime = 800;    //How frequent you want to display data  (1000 = 1 second)
String inString = "";            // string to hold input
int tempPin = 1;
int voltagePin = 2;
int motorPin = 9;
int n = 20;                      // Number of averaged adc samples
double Rsmall = 10000;           // Small Resistor of voltage divider
double Rbig = 130000;
float FSR = .256;                // FSR = Full Scale Range of ADC input
int motor_out_HIGH = 110;        // Max Motor Servo output
int motor_out_LOW = 57;          // Min Motor Servo Output
int tottle;
//----------------------------------------------------------------------------------------------------
void setup() 
{
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  motor.attach(9);
  pinMode(motorPin, OUTPUT);
  pinMode(tempPin, INPUT);
  pinMode(voltagePin, INPUT);
  ads1115.begin();
  ads1115.setGain(GAIN_SIXTEEN);  //Sets Full Scale Range to be 0.256V for high resolution
}
//----------------------------------------------------------------------------------------------------
void loop() 
{
  int throttle;
  float voltage;
  float current;
  float temp;
  float power;
 
  while (Serial.available() > 0) 
  {
    tottle = readSerial();
  }
  voltage = (analogRead(voltagePin) / 1023.0)*5*((Rsmall + Rbig)/Rsmall) * 1.0255;
  
  current = current_acq();
  power = voltage * current;
  
  temp = temp_acq();  
  if (voltage < 10)
  {
    tottle = 0;
  }
  motor_output(tottle);  
  
  Display(voltage, current, power, temp, tottle);
}
//----------------------------------------------------------------------------------------------------
void motor_output(int throttle)     // Function not currently used
{
  int motor_out = 0;
  if (throttle == 0)
  {
    motor_out = 20;
  }
  else {
    motor_out = (int)map(throttle, 1, 100, motor_out_LOW, motor_out_HIGH);
  }
  motor.write(motor_out);
}
//----------------------------------------------------------------------------------------------------
float current_acq()
{
  double adc0 = 0;
  double avg_adc0 = 0;
  float adcV;
  float current = 0;
//  int adc_vals = [0,0,0,0,0,0,0,0,0,0];
//  if (i == 10)
//  {
//    i = 0;
//  }
//  adc_vals[i] = ads1115.readADC_SingleEnded(0);  // Implements a simple moving average
//  i++;
//
//  for (int n=10; n<10; n++)
  for(int i = 0; i < n; i++)
  {
    adc0 += ads1115.readADC_SingleEnded(0);
  }
  avg_adc0 = adc0 / n;
  
  adcV = (avg_adc0 / 32765.0)*FSR;
  if ((adcV * 2000) < 20)
  {
    current = (adcV * 2000) + 1.5;
  }
  return current;
}
//----------------------------------------------------------------------------------------------------
float temp_acq()
{
  float tempB;
  float tempV;
  float temp;
  tempB = analogRead(tempPin);
  tempV = tempB *(5000/1024);
  temp = ((tempV - 500)/10) *(9/5) + 55;
  return temp;
}
//----------------------------------------------------------------------------------------------------
int readSerial()
{
    int throttle = 0;
    int inChar = Serial.read();
    if (isDigit(inChar)) {
      // convert the incoming byte to a char and add it to the string:
      inString += (char)inChar;
    }
    // if you get a newline, print the string, then the string's value:
    if (inChar == '\n') {
      throttle = inString.toInt();
      inString = "";
    }
    return throttle;
}
//----------------------------------------------------------------------------------------------------
void Display(float voltage, float current, float power, float temp, int throttle)
{
   unsigned long disp_now = millis();
   unsigned long disp_timeChange = (disp_now - disp_lastTime);
   
   if(disp_timeChange>=disp_sampleTime) {
    Serial.println("---------------------");
    Serial.println();
    Serial.print("Voltage = ");
    Serial.print(voltage);
    Serial.println("V");
    Serial.print("Current = ");
    Serial.print(current);
    Serial.println("A");
    Serial.print("Power = ");
    Serial.print(power);
    Serial.println("W");
    Serial.print("Temp = ");
    Serial.print(temp);
    Serial.println("F");
    Serial.print("Throttle = ");
    Serial.print(throttle);
    Serial.println("%");
    Serial.println();
    disp_lastTime = disp_now;
   } else {
   }
}
//----------------------------------------------------------------------------------------------------