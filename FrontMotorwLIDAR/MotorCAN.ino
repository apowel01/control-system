#include <mcp_can.h>
#include <SPI.h>
#include <TimerOne.h>
#include <math.h>
#include <stdint.h>
#include <Servo.h>
#include <Wire.h>
#include <Adafruit_ADS1015.h>

//Motor Variable Declaration
Servo motorL;  //Motor Object
Servo motorR;  //Motor Object
//Adafruit_ADS1115 ads1115L;  //ADC object
//Adafruit_ADS1115 ads1115R;  //ADC object

double disp_lastTime = 0;
double disp_sampleTime = 800;    //How frequent you want to display data  (1000 = 1 second)

//String inString = "";            // string to hold input

// Identifying Pins
//int pressurePinL =          62;   // A8
int tempPinL =              63;   // A9
int voltagePinL =           64;   // A10    *
int motorPinL =              4;
//int pressurePinR =          65;   // A11
int tempPinR =              66;   // A12
int voltagePinR =           64;   // A10    
int motorPinR =              5;             
int brakeReedPinR =         43;   //          *
int brakeReedPinL =         45;   //          *
int tensionerReedPinR =     47;   //          *
int tensionerReedPinL =     49;   //          *
int BMSDischargePin =       51;   //          *
int BMSChargePin =          53;   //          *
int brakePressPin =         68;   //A14     *
int tensionerPressPin =     69;   //A15     *

//New brake temp sensors
int brakeAirTankTempPin =   55;   //A1      * 
int tensAirTankTempPin =    56;   //A2      * 
int tensSolenoidTempPin =   57;   //A3      * 
int tensFrontPneuTempPin =  68;   //A4      * 

// Setting up Hall Sensor stuff
//The R pins on the board
const int pin22 = 22;
const int pin24 = 24;
const int pin26 = 26;
const int pin28 = 28;

const int pin30 = 30;
const int pin32 = 32;
const int pin34 = 34;
const int pin36 = 36;

//Change frequency by moving pin 2 to QA, QB, QC or QD ranked from smallest to largest
const int hallSensorOutputR = 2;
const int hallSensorOutputL = 3;
const int BandSensorOutputR = 6;

unsigned volatile int counterR = 0;
float revolutionsR;
unsigned volatile int counterL = 0;
float revolutionsL;
unsigned volatile int counterBandRight;

unsigned long currentMillis;
unsigned long lastMillis;
int RPM_R;
int RPM_L;



int n = 20;                      // Number of averaged adc samples
double Rsmall = 988;           // Small Resistor of voltage divider
double Rbig = 19850;
float FSR = .256;                // FSR = Full Scale Range of ADC input
int motor_out_HIGH = 90;         // Max Motor Servo output
int motor_out_LOW = 57;          // Min Motor Servo Output

int throttle = 0;

//CAN Variable Declaration

const int SPI_CS_PIN = 10;

MCP_CAN CAN(SPI_CS_PIN);

void setup() {
  Serial1.begin(115200);
  while (!Serial1) {
    ; // wait for serial port to connect.
  }

  // Setting up motor stuff
  motorL.attach(motorPinL);
  pinMode(motorPinL, OUTPUT);
  pinMode(tempPinL, INPUT);
  pinMode(voltagePinL, INPUT);
  motorR.attach(motorPinR);
  pinMode(motorPinR, OUTPUT);
  pinMode(tempPinR, INPUT);
  pinMode(voltagePinR, INPUT);
  pinMode(BMSDischargePin, INPUT_PULLUP);
  pinMode(BMSChargePin, INPUT_PULLUP);
  pinMode(brakePressPin, INPUT);
  pinMode(tensionerPressPin, INPUT);
  pinMode(tensionerReedPinL, INPUT_PULLUP);
  pinMode(tensionerReedPinR, INPUT_PULLUP);
  pinMode(brakeReedPinL, INPUT_PULLUP);
  pinMode(brakeReedPinR, INPUT_PULLUP);
  
  //Setting up Hall Sensor Stuff
  pinMode(pin22, OUTPUT);
  pinMode(pin24, OUTPUT);
  pinMode(pin26, OUTPUT);
  pinMode(pin28, OUTPUT);

  pinMode(pin30, OUTPUT);
  pinMode(pin32, OUTPUT);
  pinMode(pin34, OUTPUT);
  pinMode(pin36, OUTPUT);

  //Adding pin modes for new temp sensors
  pinMode(brakeAirTankTempPin, INPUT);
  pinMode(tensAirTankTempPin, INPUT);
  pinMode(tensSolenoidTempPin, INPUT);
  pinMode(tensFrontPneuTempPin, INPUT);

  //Set the R pins to LOW to start counting
  digitalWrite(pin22, LOW);
  digitalWrite(pin24, LOW);
  digitalWrite(pin26, LOW);
  digitalWrite(pin28, LOW);
  
  digitalWrite(pin30, LOW);
  digitalWrite(pin32, LOW);
  digitalWrite(pin34, LOW);
  digitalWrite(pin36, LOW);
  


  pinMode(hallSensorOutputR, INPUT_PULLUP);
  pinMode(hallSensorOutputL, INPUT_PULLUP);

  pinMode(BandSensorOutputR, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(hallSensorOutputR), tickR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(hallSensorOutputL), tickL, CHANGE);
  attachInterrupt(digitalPinToInterrupt(BandSensorOutputR), tickBand, CHANGE);


//  ads1115L.begin();
//  ads1115L.setGain(GAIN_SIXTEEN);  //Sets Full Scale Range to be 0.256V for high resolution
//  ads1115R.begin();
//  ads1115R.setGain(GAIN_SIXTEEN);  //Sets Full Scale Range to be 0.256V for high resolution


  while (CAN_OK != CAN.begin(CAN_500KBPS))              // init can bus : baudrate = 500k
  {
    Serial.println("CAN BUS Shield init fail");
    Serial.println(" Init CAN BUS Shield again");
    delay(100);
  }
  Serial.println("CAN BUS Shield init ok!");

  CAN.init_Mask(0, 0, 0xff0);                         // leave these as is
  CAN.init_Mask(1, 0, 0xff0);                         // they check the first two hexes against the filters, and let any final hex through


  CAN.init_Filt(0, 0, 0x000);                          // there are 6 filters available, we are allowing 00x, 11x, and 10x
  CAN.init_Filt(1, 0, 0x110);
  CAN.init_Filt(2, 0, 0x100);
  CAN.init_Filt(3, 0, 0x120);
  //CAN.init_Filt(4, 0, 0x108);
  //CAN.init_Filt(5, 0, 0x109);

  // Initializing Timer
  Timer1.initialize(100000);         // initialize timer1, and set a .05 second period (50000)
  Timer1.attachInterrupt(sendmessage);  // run sendmessage whenever the timer overflows
}

unsigned char stmp[8] = {0, 0, 0, 0, 0, 0, 0, 0};
bool needtosendsensor = 0;
bool launching = 0;
unsigned long timesincelaunch;

void loop() {

  //Message Reception
  unsigned char len = 0;
  unsigned char buf[8];
  unsigned long canId = 999;
  bool receivedinput = 0;

  if (CAN_MSGAVAIL == CAN.checkReceive())           // check if data coming
  {
    receivedinput = 1;
    CAN.readMsgBuf(&len, buf);    // read data,  len: data length, buf: data buf

    canId = CAN.getCanId();

    Serial.println("-----------------------------");
    Serial.print("Get data from ID: 0x");
    Serial.println(canId, HEX);

    for (int i = 0; i < len; i++) // print the data
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
      throttle = 0;
      Serial.print("F Throttle off");
      launching = false;
      CAN.sendMsgBuf(0x118, 0, 8, stmp);
      CAN.sendMsgBuf(0x128, 0, 8, stmp);
    }
    if (canId == 0x110)
    {
      throttle = 0;
      Serial.print("FR Throttle off");
      launching = false;
      CAN.sendMsgBuf(0x118, 0, 8, stmp);
    }
    if (canId == 0x120)
    {
      throttle = 0;
      Serial.print("FL Throttle off");
      launching = false;
      CAN.sendMsgBuf(0x128, 0, 8, stmp);
    }
    if (canId == 0x101)
    {
      throttle = 100;
      throttle = 100;
      Serial.print("F Max Throttle");
      launching = true; 
      timesincelaunch = millis();
      CAN.sendMsgBuf(0x118, 0, 8, stmp);
      CAN.sendMsgBuf(0x128, 0, 8, stmp);
    }
    if (canId == 0x111)
    {
      throttle = 100;
      Serial.print("FR Max Throttle");
      launching = true; 
      timesincelaunch = millis();
      CAN.sendMsgBuf(0x118, 0, 8, stmp);
    }
    if (canId == 0x121)
    {
      throttle = 100;
      Serial.print("FL Max Throttle");
      launching = true; 
      timesincelaunch = millis();
      CAN.sendMsgBuf(0x128, 0, 8, stmp);
    }
    if (canId == 0x102)
    {
      throttle = buf[7];
      throttle = throttle;
      Serial.print("F Throttle changed");
      launching = false;
      CAN.sendMsgBuf(0x118, 0, 8, stmp);
      CAN.sendMsgBuf(0x128, 0, 8, stmp);
    }
    if (canId == 0x112)
    {
      throttle = buf[7];
      Serial.print("FR Throttle changed");
      launching = false;
      CAN.sendMsgBuf(0x118, 0, 8, stmp);
    }
    if (canId == 0x122)
    {
      throttle = buf[7];
      Serial.print("FL Throttle changed");
      launching = false;
      CAN.sendMsgBuf(0x128, 0, 8, stmp);
    }

    
  }
    
    
  //Updating throttle
  if (launching == true)
  {
    throttle = (millis()-timesincelaunch)*100/15;  
  }
  if (throttle > 100)
  {
    throttle = 100;
  }
  motor_output(throttle);
  
  // Hall Sensing
  currentMillis = millis();
  revolutionsR = counterR/14.0;
  revolutionsL = counterL/14.0;
  
  if( (currentMillis-lastMillis)>100){
    counterR = 0;
    counterL = 0;
    RPM_R = revolutionsR*10*60;
    RPM_L = revolutionsL*10*60;
    lastMillis = currentMillis;
  }

  
  //LIDAR SENSING
  char resultBuffer[8];
  int bufferIndex = 0;
  int c = 0;
  
  // Request a distance.
  Serial1.write('d');
  
  // Wait for distance response.
  while(c != '\n') {
    while (!Serial1.available());
    c = Serial1.read();
    
    resultBuffer[bufferIndex++] = c;
  }

  // Process response into distance value.
  resultBuffer[bufferIndex - 2] = 0;
  float distance = atof(resultBuffer);

  //Message Sending, with Timer1 delay
  
  if (needtosendsensor)
  {   
    
    //Sending LIDAR Data
    stmp[0] = 0;
    stmp[1] = 0;
    stmp[2] = 0;
    stmp[3] = 0;
    stmp[4] = 0;
    stmp[5] = 0;    
    stmp[6] = highByte((int) distance);
    stmp[7] = lowByte((int) distance);
//    Serial.print(stmp);    
    CAN.sendMsgBuf(0x419, 0, 8, stmp);
    
    //Sending Band Sensor Data
    stmp[6] = highByte((int) counterBandRight);
    stmp[7] = lowByte((int) counterBandRight);
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x41a, 0, 8, stmp);
    
    // Generating Motor Data Packets
    float voltageL;
//    float currentL;
    float tempL;
//    float powerL;
    float voltageR;
//    float currentR;
    float tempR;
    float brakePressure;
    float tensionerPressure;
//    float powerR;
    voltageL = (analogRead(voltagePinL) / 1023.0) * 5 * ((Rsmall + Rbig) / Rsmall) * 1.0255;
//    currentL = current_acq("L");
//    powerL = voltageL * currentL;
    tempL = temp_acq(tempPinL);
    voltageR = (analogRead(voltagePinR) / 1023.0) * 5 * ((Rsmall + Rbig) / Rsmall) * 1.0255;
//    currentR = current_acq("R");
//    powerR = voltageR * currentR;
    tempR = temp_acq(tempPinR);
    
    // Generating Pressure Readings
    brakePressure = press_acq(brakePressPin);
    tensionerPressure = press_acq(tensionerPressPin);

    // Generating Other Temp Readings
    float brakeTankTemp;
    float tensTankTemp;
    float tensSolenoidTemp;
    float tensFrontPneuTemp;
    
    brakeTankTemp = temp_acq(brakeAirTankTempPin);
    tensTankTemp = temp_acq(tensAirTankTempPin);
    tensSolenoidTemp = temp_acq(tensSolenoidTempPin);
    tensFrontPneuTemp = temp_acq(tensFrontPneuTempPin);
    
    
    
    // Sending Motor Data Packets
    stmp[1] = highByte((int) RPM_R);
    stmp[2] = lowByte((int) RPM_R);    
    stmp[3] = highByte((int) voltageR);
    stmp[4] = lowByte((int) voltageR);
    stmp[5] = highByte((int) tempR);
    stmp[6] = lowByte((int) tempR);
    stmp[7] = throttle;
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x119, 0, 8, stmp);
    stmp[1] = highByte((int) RPM_L);
    stmp[2] = lowByte((int) RPM_L);
    stmp[3] = highByte((int) voltageL);
    stmp[4] = lowByte((int) voltageL);
    stmp[5] = highByte((int) tempL);
    stmp[6] = lowByte((int) tempL);
    stmp[7] = throttle;
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x129, 0, 8, stmp);
    
    //Sending BMS Data Packet
    stmp[1] = 0;
    stmp[2] = 0;
    stmp[3] = 0;
    stmp[4] = 0;
    stmp[5] = 0;
    stmp[6] = digitalRead(BMSChargePin);
    stmp[7] = digitalRead(BMSDischargePin);
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x51a, 0, 8, stmp);

    //Sending Brake Packet
    stmp[4] = highByte((int) brakeTankTemp);
    stmp[5] = lowByte((int) brakeTankTemp);
    stmp[6] = highByte((int) brakePressure);
    stmp[7] = lowByte((int) brakePressure);
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x20a, 0, 8, stmp);

    //Sending Tensioner Packet
    stmp[0] = highByte((int) tensSolenoidTemp);
    stmp[1] = lowByte((int) tensSolenoidTemp);
    stmp[2] = highByte((int) tensFrontPneuTemp);
    stmp[3] = lowByte((int) tensFrontPneuTemp);
    stmp[4] = highByte((int) tensTankTemp);
    stmp[5] = lowByte((int) tensTankTemp);
    stmp[6] = highByte((int) tensionerPressure);
    stmp[7] = lowByte((int) tensionerPressure);
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x30a, 0, 8, stmp);    

    //Sending Brake Reed Switch Data
    stmp[1] = 0;
    stmp[2] = 0;
    stmp[3] = 0;
    stmp[4] = 0;
    stmp[5] = 0;
    stmp[6] = 0;
    stmp[7] = digitalRead(brakeReedPinR);
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x219, 0, 8, stmp);
    stmp[7] = digitalRead(brakeReedPinL);
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x229, 0, 8, stmp);

    //Sending Tensioner Reed Switch Data
    stmp[7] = digitalRead(tensionerReedPinR);
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x319, 0, 8, stmp);
    stmp[7] = digitalRead(tensionerReedPinL);
//    Serial.print(stmp);
    CAN.sendMsgBuf(0x329, 0, 8, stmp);

    
        
    //Resetting Timer
    needtosendsensor = 0;
  }
  //Display(voltage, current, power, temp, throttle);
}


//----------------------------------------------------------------------------------------------------

void sendmessage() {
  needtosendsensor = 1;
}

//----------------------------------------------------------------------------------------------------
void motor_output(int throttle)
{
  int motor_out = 0;
  if (throttle == 0)
  {
    motor_out = 20;
  }
  else
  {
    motor_out = (int)map(throttle, 1, 100, motor_out_LOW, motor_out_HIGH);
  }
    motorL.write(motor_out);
    motorR.write(motor_out);

}

//----------------------------------------------------------------------------------------------------

void tickR() {
  counterR = counterR + 1;
}

void tickL() {
  counterL = counterL + 1;
}

void tickBand() {
  counterBandRight = counterBandRight + 1;
}
//----------------------------------------------------------------------------------------------------

float temp_acq(int pin)
{
  float tempB;
  float tempV;
  float temp;
  
  tempB = analogRead(pin);
  tempV = tempB * (5000 / 1024);

  temp = ((tempV - 500) / 10) * (9 / 5) + 55;
  return temp;
}

//----------------------------------------------------------------------------------------------------


float press_acq(int pin)
{
  float pressureB;
  float pressureV;
  float pressure;

  pressureB = analogRead(pin);
  pressureV = pressureB *(5000/1024);
  pressure = 71.325*pressureV + 157.35;
  return pressure;
}


//----------------------------------------------------------------------------------------------------

//int readSerial() // Unused currently
//{
//  int throttle = 0;
//  int inChar = Serial.read();
//  if (isDigit(inChar)) {
//    // convert the incoming byte to a char and add it to the string:
//    inString += (char)inChar;
//  }
//  // if you get a newline, print the string, then the string's value:
//  if (inChar == '\n') {
//
//    throttle = inString.toInt();
//    inString = "";
//  }
//  return throttle;
//}

//----------------------------------------------------------------------------------------------------

//void Display(float voltage, float current, float power, float temp, int throttle) // Unused currently
//{
//  unsigned long disp_now = millis();
//  unsigned long disp_timeChange = (disp_now - disp_lastTime);
//
//  if (disp_timeChange >= disp_sampleTime) {
//    Serial.println();
//    Serial.print("Voltage = ");
//    Serial.print(voltage);
//    Serial.println("V");
//    Serial.print("Current = ");
//    Serial.print(current);
//    Serial.println("A");
//    Serial.print("Power = ");
//    Serial.print(power);
//    Serial.println("W");
//    //    Serial.print("Temp = ");
//    //    Serial.print(temp);
//    //    Serial.println("F");
//    //    Serial.println();
//    Serial.print("Throttle = ");
//    Serial.print(throttle);
//    Serial.println("%");
//    //    Serial.println();
//    //    Serial.println("---------------------");
//
//    disp_lastTime = disp_now;
//  } else {
//  }
//}

//----------------------------------------------------------------------------------------------------

//----------------------------------------------------------------------------------------------------
//float current_acq(char WhichMotor)
//{
//  double adc0 = 0;
//  double avg_adc0 = 0;
//  float adcV;
//  float current = 0;
//  //  int adc_vals = [0,0,0,0,0,0,0,0,0,0];
//  //  if (i == 10)
//  //  {
//  //    i = 0;
//  //  }
//  //  adc_vals[i] = ads1115.readADC_SingleEnded(0);  // Implements a simple moving average
//  //  i++;
//  //
//  //  for (int n=10; n<10; n++)
//  if (WhichMotor == "L")
//  {
//    for (int i = 0; i < n; i++)
//    {
//      adc0 += ads1115L.readADC_SingleEnded(0);
//    }
//  }
//  else
//  {
//    for (int i = 0; i < n; i++)
//    {
//      adc0 += ads1115R.readADC_SingleEnded(0);
//    }
//  }
//  avg_adc0 = adc0 / n;
//
//  adcV = (avg_adc0 / 32765.0) * FSR;
//  if ((adcV * 2000) < 20)
//  {
//    current = (adcV * 2000) - 5;
//  }
//  return current;
//}

//unsigned int hexToDec(String hexString) {  // Function not currently used
//
//  unsigned int decValue = 0;
//  int nextInt;
//
//  for (int i = 0; i < hexString.length(); i++) {
//
//    nextInt = int(hexString.charAt(i));
//    if (nextInt >= 48 && nextInt <= 57) nextInt = map(nextInt, 48, 57, 0, 9);
//    if (nextInt >= 65 && nextInt <= 70) nextInt = map(nextInt, 65, 70, 10, 15);
//    if (nextInt >= 97 && nextInt <= 102) nextInt = map(nextInt, 97, 102, 10, 15);
//    nextInt = constrain(nextInt, 0, 15);
//
//    decValue = (decValue * 16) + nextInt;
//  }
//
//  return decValue;
//}
