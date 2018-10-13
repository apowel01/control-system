/*
  MOSI - pin 11
  MISO - pin 12
  CLK - pin 13
  CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN)
*/
#include <SPI.h>
#include <SD.h>
File testFile;

int CSPIN = 4;

void setup() 
{
  // Open serial communication
  Serial.begin(9600);
  while (!Serial) {}
  SDInit();
}

void loop() 
{
  readAndWrite();
}

void SDInit()
{
  Serial.print("Initializing SD card... ");
  if (!SD.begin(CSPIN))
  {
    Serial.println("initialization failed!");
    while(1) {}
  }

  Serial.println("initialization done.");
  // Check to see if the file exists:
  if (SD.exists("TEST.CSV")) 
  {
    Serial.println("TEST.CSV exists.");
    Serial.print("Removing test.csv... ");
    SD.remove("TEST.CSV");
    Serial.println("done");
  } 
  else 
  {
    Serial.println("TEST.CSV doesn't exist.");
  }

  testFile = SD.open("test.csv", FILE_WRITE);
}

void readAndWrite()
{
  if (Serial.available())
  {
    String input = Serial.readString();
    input.trim();
    if (input == "Stop")
    {
      testFile.close();
      while(1) {}
    }
    testFile.println(input);
    Serial.print("Wrote: ");
    Serial.println(input);
  }
}
