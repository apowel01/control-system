#include <mcp_can.h>
#include <SPI.h>
#include <TimerOne.h>
#include <math.h>
#include <stdint.h>

const int SPI_CS_PIN = 10;

MCP_CAN CAN(SPI_CS_PIN);   

void setup() {
  Serial.begin(115200);

  // Check what baud rate the SF11 is using for serial communication in the SF11 settings menu. (Communication menu -> Serial port baud rate)
  Serial1.begin(115200);

  while (CAN_OK != CAN.begin(CAN_500KBPS))              // init can bus : baudrate = 500k
    {
        Serial.println("CAN BUS Shield init fail");
        Serial.println(" Init CAN BUS Shield again");
        delay(100);
    }
    Serial.println("CAN BUS Shield init ok!");

    CAN.init_Mask(0, 0, 0xff0);                         // leave these as is
    CAN.init_Mask(1, 0, 0xff0);                         // they check the first two hexes against the filters, and let any final hex through

 
    CAN.init_Filt(0, 0, 0x000);                          // there are 6 filters available, we are allowing 00x, 40x, 41x
    CAN.init_Filt(1, 0, 0x400);                          
    CAN.init_Filt(2, 0, 0x410);                          
    //CAN.init_Filt(3, 0, 0x107);                        
    //CAN.init_Filt(4, 0, 0x108);                          
    //CAN.init_Filt(5, 0, 0x109);                          

    // Initializing Timer
    Timer1.initialize(500000);         // initialize timer1, and set a 1/2 second period
    Timer1.attachInterrupt(sendmessage);  // run sendmessage whenever the timer overflows
  
}

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
//  if (receivedinput == 1)
//  {
//    if (canId == 0x000 || canId == 0x100)
//        {
//          throttle = 0;
//          Serial.print("Throttle off");
//          CAN.sendMsgBuf(0x118, 0, 8, stmp);
//        }
//    if (canId == 0x101 || canId == 0x111)
//        {
//          throttle = 100;
//          Serial.print("Max Throttle");
//          CAN.sendMsgBuf(0x118, 0, 8, stmp);
//        }
//    if (canId == 0x102 || canId == 0x112)
//        {
//          throttle = buf[7];
//          Serial.print("Throttle changed");
//          CAN.sendMsgBuf(0x118, 0, 8, stmp);
//        }
//}
  
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
  
  Serial.print(distance);
  Serial.println(" m");
  
  //Message Sending, with Timer1 delay
    if (needtosendsensor)
        {  
        stmp[6] = highByte((int) distance);
        stmp[7] = lowByte((int) distance);    
        
        CAN.sendMsgBuf(0x419, 0, 8, stmp);
        needtosendsensor = 0;
        }
}
