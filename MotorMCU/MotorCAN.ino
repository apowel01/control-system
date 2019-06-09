#include <mcp_can.h>
#include <SPI.h>
#include <TimerOne.h>
#include <math.h>
#include <stdint.h>
#include <Servo.h>
#include <Wire.h>
#include <Adafruit_ADS1015.h>

//Motor Variable Declaration
Servo motor;  //Motor Object
Adafruit_ADS1115 ads1115;  //ADC object


double disp_lastTime = 0;
double disp_sampleTime = 800;    //How frequent you want to display data  (1000 = 1 second)

String inString = "";            // string to hold input

int pressurePin = 3;
int tempPin = 1;
int voltagePin = 2;
int motorPin = 9;

int n = 20;                      // Number of averaged adc samples
double Rsmall = 10000;           // Small Resistor of voltage divider
double Rbig = 150000;
float FSR = .256;                // FSR = Full Scale Range of ADC input
int motor_out_HIGH = 90;        // Max Motor Servo output
int motor_out_LOW = 57;          // Min Motor Servo Output

int throttle = 100;

//CAN Variable Declaration

const int SPI_CS_PIN = 10;

MCP_CAN CAN(SPI_CS_PIN);   

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  // Setting up motor stuff
  motor.attach(9);
  pinMode(motorPin, OUTPUT);
  pinMode(tempPin, INPUT);
  pinMode(voltagePin, INPUT);
  ads1115.begin();
  ads1115.setGain(GAIN_SIXTEEN);  //Sets Full Scale Range to be 0.256V for high resolution


    while (CAN_OK != CAN.begin(CAN_500KBPS))              // init can bus : baudrate = 500k
    {
        Serial.println("CAN BUS Shield init fail");
        Serial.println(" Init CAN BUS Shield again");
        delay(100);
    }
    Serial.println("CAN BUS Shield init ok!");

    CAN.init_Mask(0, 0, 0xff0);                         // leave these as is
    CAN.init_Mask(1, 0, 0xff0);                         // leave these as is, they check the first two hexes against the filters, and let any final hex through


    /*
     * set filter, we can receive id from 0x04 ~ 0x09
     */
    CAN.init_Filt(0, 0, 0x000);                          // there are 6 filter in mcp2515
    CAN.init_Filt(1, 0, 0x110);                          // there are 6 filter in mcp2515

    CAN.init_Filt(2, 0, 0x100);                          // there are 6 filter in mcp2515
    //CAN.init_Filt(3, 0, 0x107);                          // there are 6 filter in mcp2515
    //CAN.init_Filt(4, 0, 0x108);                          // there are 6 filter in mcp2515
    //CAN.init_Filt(5, 0, 0x109);                          // there are 6 filter in mcp2515

    // Initializing Timer
    Timer1.initialize(500000);         // initialize timer1, and set a 1/2 second period
    Timer1.attachInterrupt(sendmessage);  // run sendmessage whenever the timer overflows

}

unsigned char stmp[8] = {0, 0, 0, 0, 0, 0, 0, 0};
bool needtosendsensor = 0;

void loop() {

//Message Reception
    unsigned char len = 0;
    unsigned char buf[8];
    unsigned long canId = 999;
    bool receivedinput = 0;

    if(CAN_MSGAVAIL == CAN.checkReceive())            // check if data coming
    {
        receivedinput = 1;
        CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf

        canId = CAN.getCanId();
        
        Serial.println("-----------------------------");
        Serial.print("Get data from ID: 0x");
        Serial.println(canId, HEX);

        for(int i = 0; i<len; i++)    // print the data
        {
            Serial.print(buf[i], HEX);
            Serial.print("\t");
        }
        Serial.println();
    }

//Message Processing
if (receivedinput == 1)
{
if (canId == 0x000 || canId == 0x100)
        {
        throttle = 0;
        Serial.print("Throttle off");
        CAN.sendMsgBuf(0x118, 0, 8, stmp);
        }
if (canId == 0x101 || canId == 0x111)
        {
        throttle = 100;
        Serial.print("Max Throttle");
        CAN.sendMsgBuf(0x118, 0, 8, stmp);
        }
if (canId == 0x102 || canId == 0x112)
        {
        throttle = buf[7];
        Serial.print("Throttle changed");
        CAN.sendMsgBuf(0x118, 0, 8, stmp);
        }
}

//Motor Control
  float voltage;
  float current;
  float temp;
  float power;
 
//  while (Serial.available() > 0) 
//  {
//    throttle = readSerial();
//  }

  voltage = (analogRead(voltagePin) / 1023.0)*5*((Rsmall + Rbig)/Rsmall) * 1.0255;
  
  current = current_acq();

  power = voltage * current;
  
  temp = temp_acq();  

  motor_output(throttle);

//Message Sending, with Timer1 delay
    if (needtosendsensor)
        {
        stmp[3] = highByte((int) voltage);
        stmp[4] = lowByte((int) voltage);
        stmp[5] = highByte((int) temp);  
        stmp[6] = lowByte((int) temp);
        stmp[7] = throttle;    
    CAN.sendMsgBuf(0x119, 0, 8, stmp);
        needtosendsensor = 0;
        }
//Display(voltage, current, power, temp, throttle);
}


//----------------------------------------------------------------------------------------------------

void sendmessage() {
  needtosendsensor = 1;
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

//
//float press_acq()
//{
//  float pressureB;
//  float preesureP;
//  float pressure;
//
//  pressureB = analogRead(pressurePin);
//  pressureV = pressureB *(5000/1024);
//  pressure = 71.325*pressureV + 157.35;
//  return temp;
//}


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
//    Serial.print("Temp = ");
//    Serial.print(temp);
//    Serial.println("F");
//    Serial.println();
    Serial.print("Throttle = ");
    Serial.print(throttle);
    Serial.println("%");
//    Serial.println();
//    Serial.println("---------------------");

    disp_lastTime = disp_now;
   } else {
   }
}

//----------------------------------------------------------------------------------------------------

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
    current = (adcV * 2000) - 5;
  }
  return current;
}

unsigned int hexToDec(String hexString) {
  
  unsigned int decValue = 0;
  int nextInt;
  
  for (int i = 0; i < hexString.length(); i++) {
    
    nextInt = int(hexString.charAt(i));
    if (nextInt >= 48 && nextInt <= 57) nextInt = map(nextInt, 48, 57, 0, 9);
    if (nextInt >= 65 && nextInt <= 70) nextInt = map(nextInt, 65, 70, 10, 15);
    if (nextInt >= 97 && nextInt <= 102) nextInt = map(nextInt, 97, 102, 10, 15);
    nextInt = constrain(nextInt, 0, 15);
    
    decValue = (decValue * 16) + nextInt;
  }
  
  return decValue;
}
