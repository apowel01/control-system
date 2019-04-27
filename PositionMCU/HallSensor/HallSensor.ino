//Decoder documentations
//http://www.ti.com/lit/ds/symlink/sn74ls90.pdf


//The R pins on the board
const int pin22 = 22;
const int pin24 = 24;
const int pin26 = 26;
const int pin28 = 26;

//Change frequency by moving pin 2 to QA, QB, QC or QD ranked from smallest to largest
const int hallSensorOutput = 2;

unsigned volatile int counter = 0;
float revolutions;

unsigned long currentMillis;
unsigned long lastMillis;
int RPM;

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(9600);
  pinMode(pin22, OUTPUT);
  pinMode(pin24, OUTPUT);
  pinMode(pin26, OUTPUT);
  pinMode(pin28, OUTPUT);

  //Set the R pins to LOW to start counting
  digitalWrite(pin22, LOW);
  digitalWrite(pin24, LOW);
  digitalWrite(pin26, LOW);
  digitalWrite(pin28, LOW);
  
  pinMode(hallSensorOutput, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(hallSensorOutput), tick, CHANGE);
}


void loop() {
  currentMillis = millis();
  revolutions = counter/14.0;
  
  if( (currentMillis-lastMillis)>100){
    counter = 0;
    RPM = revolutions*10*60;
    lastMillis = currentMillis;
  }
  Serial.print(RPM);
  Serial.println(" RPMs");

}

void tick() {
  counter = counter + 1;
}
