const int pin3 = 3;
const int pin22 = 22;
const int pin24 = 24;
const int pin26 = 26;
const int pin28 = 26;
const int interruptPin = 2;

volatile int counter = 0;
float revolutions;



void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  Serial.begin(9600);
  pinMode(pin3, OUTPUT);
  pinMode(pin22, OUTPUT);
  pinMode(pin24, OUTPUT);
  pinMode(pin26, OUTPUT);
  pinMode(pin28, OUTPUT);

  digitalWrite(pin22, LOW);
  digitalWrite(pin24, LOW);
  digitalWrite(pin26, LOW);
  digitalWrite(pin28, LOW);
  
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), tick, CHANGE);
}


void loop() {
  digitalWrite(pin3, HIGH);
//  Serial.println(digitalRead(interruptPin2));
  delay(60);
  digitalWrite(pin3, LOW);
  delay(60);
  revolutions = counter/14;
  Serial.println(revolutions);
}

void tick() {
  counter = counter + 1;
}
