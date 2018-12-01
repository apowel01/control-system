/* Erik Bruenner
 * Bryce Campbell
 * Monty Choy
 *
 * 11/3/18
 *
 * Last Updated - 11/5/18
 *
 * Code for laser sensor interrupt.
 */

#include <SoftwareSerial.h>
#include <Wire.h>

//defines the slave address of the uno
#define SLAVE_ADDRESS 0x04

//adjust this delay as needed (hopefully none once we hood it up and test)
#define COUNTER_DELAY 100 // wait this amount of time after each interupt

// wait this amount of time after each interupt
#define LASER_DELAY 1000 

// distance between reflective tape in feet
#define LASER_TICK_DISTANCE 100 

// distance between reflective tape in feet
#define COUNTER_TICK_DISTANCE 100 

//String array denoting requestType, this must match exactly with the list on the PI
const String requestType[] = {"HALL_POSITION", "LASER_POSITION", "STRIPE_COUNT", "PERCENT_ERROR", "VELOCITY", "ACCELERATION", "RESET"};

//keeps track of request type so different data can be sent in the future
String request;

// pin for laser sensor interrupt
int laserSensorPin = 2;

//sets the counter Sensor pin
const int counterSensorPin = 3; 

//timer to make sure we dont get too many signals
volatile double counterTime = millis();

// timer to prevent the interrupt from being called mulltiple times per strip.
volatile double laserTime = millis(); 

// the number of ticks the pod has traveled
volatile int totalTicksLaser = 0;

// the number of ticks the pod has traveled
volatile int totalTicksCounter = 0;

int number = 0;

float oldTime = millis();
float oldPositon = 0;

int velocity = 0;
int acceleration = 0;

/*
 * Main loop
 */
void loop() {
  Serial.println("Laser: " + (String)totalTicksLaser + " - Counter: " + (String)totalTicksCounter); // print the total ticks for debug

  float deltaTime = millis() - oldTime; // getting delta time since last loop call
  float deltaPosition = get_hall_position() - oldPositon; // getting delta position since last loop call

  int oldVelocity = velocity; // store velocity from last tick
  
  update_velocity(deltaTime, deltaPosition); // get new velocity
  update_acceleration(deltaTime, velocity - oldVelocity); // get new acceleration using velocity from last tick and the new velocity we just found

  oldTime = millis(); // set current time to old time for next tick
  oldPositon = get_hall_position(); // set current position to old position for next tick

  delay(1000);
}

/*
 * Interrupt service routine for the counter
 *
 *  Waits for laserDelay amount of milliseconds and then increments the ticksSinceLastCheck when the counter detects a signal
 */
void counter_isr() {
  if(counterTime + COUNTER_DELAY < millis()) // pause for laserDelay number of millis after interrupt is triggered
  {
    //Serial.println("Interrupt");
    totalTicksCounter++; // increment number of ticks since the last check
    counterTime = millis();
  }
}


/*
 * Interrupt service routine for the laser sensor
 *
 *  Waits for laserDelay amount of milliseconds and then increments the ticksSinceLastCheck when the laser sees
 *  a reflective strip.
 */
void laser_isr() {
  if(laserTime + LASER_DELAY < millis()) // pause for laserDelay number of millis after interrupt is triggered
  {
    //Serial.println("Interrupt");
    totalTicksLaser++; // increment number of ticks since the last check
    laserTime = millis();
  }
}

/*
 * Sets up the interrupt for the counter
 */
void counter_setup()
{
  pinMode(counterSensorPin, INPUT_PULLUP);
  // TODO: determine if this should be FALLING or LOW
  attachInterrupt(digitalPinToInterrupt(counterSensorPin), counter_isr, FALLING); // trigger interrupt when signal from laser falls to 0
}

/*
 * Sets up the interrupt for the laser sensor
 */
void laser_setup()
{
  pinMode(laserSensorPin, INPUT_PULLUP);
  // TODO: determine if this should be FALLING or LOW
  attachInterrupt(digitalPinToInterrupt(laserSensorPin), laser_isr, FALLING); // trigger interrupt when signal from laser falls to 0
}

/*
 * returns the position of the pod down the track in feet based on the number of reflective strips it has passed
 */
int get_laser_position()
{
  return totalTicksLaser * LASER_TICK_DISTANCE;
}

/*
 * Temporary function repplace code and this comment when implemented
 */
int get_hall_position()
{
  return totalTicksCounter * COUNTER_TICK_DISTANCE;
}

//resets count when an I2C signal is encountered by 
void reset_count()
{
  totalTicksCounter = 0;
  totalTicksLaser = 0;
}
/*
 * Pod velocity estimation in centimeters per second 
 */
int update_velocity(float deltaTime, int deltaPosition)
{
	return deltaPosition/deltaTime;
}

/*
 * Pod acceleration estimation in centimeters per second squared
 */
int update_acceleration(float deltaTime, float deltaVelocity)
{
	return deltaVelocity/deltaTime;
}

/*
 * returns thee percentage error of the laser sensors compared to the hall sensors as a deciamal
 * for example if the laser sensor is ahead of the hall sensor by one band this function will return 1
 */
double get_position_error()
{
  int laser = get_laser_position();
  int hall = get_hall_position();
  return (laser - hall)/LASER_TICK_DISTANCE;
}

// callback for sending data
void send_data(){
	// based on what type of data the pi requested send the appropriate value
      if(request == "HALL_POSITION") {
        Wire.write(get_hall_position());
        
      } else if(request == "LASER_POSITION") {
        Wire.write(get_laser_position());
        
      } else if(request == "STRIPE_COUNT") {
      	Wire.write(totalTicksLaser);

      } else if(request  == "PERCENT_ERROR") {
        Wire.write((int)(get_position_error()*100));
        
      } else if(request  == "VELOCITY") {
      	Wire.write(velocity);

      } else if(request  == "ACCELERATION") {
      	Wire.write(acceleration);

      } else if(request == "RESET") {
        reset_count();
        Wire.write("0");
        
      }
      
}

void receive_data(int byteCount)
{
  while (Wire.available())
  {
     request = requestType[Wire.read()];
  }
}


//initializes this arduino as an I2C slave, establishes callbacks
void I2C_setup()
{
    // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onRequest(send_data);
  Wire.onReceive(receive_data);
}

void setup() {
  Serial.begin(9600); // start serial for output

  // initialize laser interupt
  laser_setup();

  // initialize laser interupt
  counter_setup();

  I2C_setup();

  Serial.println("Ready!");
}
