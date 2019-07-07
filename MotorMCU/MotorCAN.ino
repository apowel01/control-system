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
int pressurePinL = 62; // A8
int tempPinL = 63;     // A9
int voltagePinL = 64;  // A10
int motorPinL = 2;
int pressurePinR = 65; // A11
int tempPinR = 66;     // A12
int voltagePinR = 67;  // A13
int motorPinR = 3;
int BMSdischarge = 51;
int BMScharge = 53;


int n = 20;                      // Number of averaged adc samples
double Rsmall = 10000;           // Small Resistor of voltage divider
double Rbig = 150000;
float FSR = .256;                // FSR = Full Scale Range of ADC input
int motor_out_HIGH = 90;         // Max Motor Servo output
int motor_out_LOW = 57;          // Min Motor Servo Output

int throttleL = 0;
int throttleR = 0;

//CAN Variable Declaration

const int SPI_CS_PIN = 10;

MCP_CAN CAN(SPI_CS_PIN);

void setup() {
	Serial.begin(115200);
	while (!Serial) {
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
	pinMode(BMSdischarge, INPUT_PULLUP);
	pinMode(BMScharge, INPUT_PULLUP);

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
			throttleR = 0;
			throttleL = 0;
			Serial.print("F Throttle off");
			CAN.sendMsgBuf(0x118, 0, 8, stmp);
			CAN.sendMsgBuf(0x128, 0, 8, stmp);
		}
		if (canId == 0x110)
		{
			throttleR = 0;
			Serial.print("FR Throttle off");
			CAN.sendMsgBuf(0x118, 0, 8, stmp);
		}
		if (canId == 0x120)
		{
			throttleL = 0;
			Serial.print("FL Throttle off");
			CAN.sendMsgBuf(0x128, 0, 8, stmp);
		}
		if (canId == 0x101)
		{
			throttleR = 100;
			throttleL = 100;
			Serial.print("F Max Throttle");
			CAN.sendMsgBuf(0x118, 0, 8, stmp);
			CAN.sendMsgBuf(0x128, 0, 8, stmp);
		}
		if (canId == 0x111)
		{
			throttleR = 100;
			Serial.print("FR Max Throttle");
			CAN.sendMsgBuf(0x118, 0, 8, stmp);
		}
		if (canId == 0x121)
		{
			throttleL = 100;
			Serial.print("FL Max Throttle");
			CAN.sendMsgBuf(0x128, 0, 8, stmp);
		}
		if (canId == 0x102)
		{
			throttleR = buf[7];
			throttleL = throttleR;
			Serial.print("F Throttle changed");
			CAN.sendMsgBuf(0x118, 0, 8, stmp);
			CAN.sendMsgBuf(0x128, 0, 8, stmp);
		}
		if (canId == 0x112)
		{
			throttleR = buf[7];
			Serial.print("FR Throttle changed");
			CAN.sendMsgBuf(0x118, 0, 8, stmp);
		}
		if (canId == 0x122)
		{
			throttleL = buf[7];
			Serial.print("FL Throttle changed");
			CAN.sendMsgBuf(0x128, 0, 8, stmp);
		}

		motor_output(throttleL, "L");
		motor_output(throttleR, "R");
	}

	//  while (Serial.available() > 0)
	//  {
	//    throttle = readSerial();
	//  }



	//Message Sending, with Timer1 delay
	if (needtosendsensor)
	{
		
		// Generating Motor Data Packets
		float voltageL;
//    float currentL;
		float tempL;
//    float powerL;
		float voltageR;
//    float currentR;
		float tempR;
//    float powerR;
		voltageL = (analogRead(voltagePinL) / 1023.0) * 5 * ((Rsmall + Rbig) / Rsmall) * 1.0255;
//    currentL = current_acq("L");
//    powerL = voltageL * currentL;
		tempL = temp_acq("L");
		voltageR = (analogRead(voltagePinR) / 1023.0) * 5 * ((Rsmall + Rbig) / Rsmall) * 1.0255;
//    currentR = current_acq("R");
//    powerR = voltageR * currentR;
		tempR = temp_acq("R");
		
		// Sending Motor Data Packets
		stmp[3] = highByte((int) voltageR);
		stmp[4] = lowByte((int) voltageR);
		stmp[5] = highByte((int) tempR);
		stmp[6] = lowByte((int) tempR);
		stmp[7] = throttleR;
		CAN.sendMsgBuf(0x119, 0, 8, stmp);
		stmp[3] = highByte((int) voltageL);
		stmp[4] = lowByte((int) voltageL);
		stmp[5] = highByte((int) tempL);
		stmp[6] = lowByte((int) tempL);
		stmp[7] = throttleL;
		CAN.sendMsgBuf(0x129, 0, 8, stmp);
		
		//Sending BMS Data Packet
		stmp[3] = 0;
		stmp[4] = 0;
		stmp[5] = 0;
		stmp[6] = digitalRead(BMScharge);
		stmp[7] = digitalRead(BMSdischarge);
		CAN.sendMsgBuf(0x51a, 0, 8, stmp);
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

void motor_output(int throttle, char WhichMotor)
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
	if (WhichMotor == "L")
	{
		motorL.write(motor_out);
	}
	else
	{
		motorR.write(motor_out);
	}

}

//----------------------------------------------------------------------------------------------------

float temp_acq(char WhichMotor)
{
	float tempB;
	float tempV;
	float temp;
	if (WhichMotor == "L")
	{
		tempB = analogRead(tempPinL);
	}
	else
	{
		tempB = analogRead(tempPinR);
	}
	tempV = tempB * (5000 / 1024);

	temp = ((tempV - 500) / 10) * (9 / 5) + 55;
	return temp;
}

//----------------------------------------------------------------------------------------------------

//
//float press_acq()
//{
//  float pressureB;
//  float pressureV;
//  float pressure;
//
//  pressureB = analogRead(pressurePin);
//  pressureV = pressureB *(5000/1024);
//  pressure = 71.325*pressureV + 157.35;
//  return temp;
//}


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