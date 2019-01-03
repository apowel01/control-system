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

// TODO: dont forget to remove this with the other code if/when we determine it is not needed
//adjust this delay as needed (hopefully none once we hood it up and test)
#define COUNTER_DELAY 100 // wait this amount of time after each interupt

// distance to wait before re-activating laser sensor after it sees a band
//     this way we dont risk double counting a band
#define LASER_DELAY_DISTANCE 5000

// distance between reflective tape in cetimeters
#define LASER_TICK_DISTANCE 3048 // num_feet * 30.48

// distance the pod travels between ticks on the final hall counter
//     TODO: replace this value once we know wheel size.
#define COUNTER_TICK_DISTANCE 100 // TODO find what this value should be

// String array denoting requestType, THIS MUST EXACTLY MATCH WHAT IS ON THE PI
const String requestType[] = {"HALL_POSITION", "LASER_POSITION", "STRIPE_COUNT", "PERCENT_ERROR", "VELOCITY", "ACCELERATION", "RESET"};

//keeps track of request type so different data can be sent in the future
String request;

// pin for laser sensor interrupt
const int laserSensorPin = 2;

//sets the counter Sensor pin
const int counterSensorPin = 3; 

//timer to make sure we dont get too many signals
volatile double counterTime = millis();

// holds the distance the pod has gone since the last successfull laser interupt to ensure the pod has traveled far enough that a band will not be double counted
volatile double laserDistanceDelta = 0; 

// the number of bands the pod has traveled past
volatile int totalTicksLaser = 0;

// the number of ticks on the final hall counter the pod has traveled
volatile int totalTicksCounter = 0;

// the distance as measured by the hall sensors and verified with the laser sensors
volatile int totalCounterDistance = 0;

float oldTime = millis();
float oldPositon = 0;

int velocity = 0;
int acceleration = 0;

/*
 * Main loop
 */
void loop() {

  // TODO: comment this when testing is done
  Serial.println("Laser: " + (String)totalTicksLaser + " - Counter: " + (String)totalTicksCounter); // print the total ticks for debug

  // TODO: we could use a running average for velocity and acceleration if the data is inconsistant

  // getting delta time since last loop call
  float deltaTime = millis() - oldTime; 
  
  // getting delta position since last loop call
  float deltaPosition = get_hall_position() - oldPositon;

  // store velocity from last tick
  int oldVelocity = velocity;
  
  // get new velocity
  update_velocity(deltaTime, deltaPosition);

  // get new acceleration using velocity from last tick and the new velocity we just found
  update_acceleration(deltaTime, velocity - oldVelocity);

  // set current time to old time for next tick
  oldTime = millis();

  // set current position to old position for next tick
  oldPositon = get_hall_position();


  // change laser distace delta by hall position distance delta this means that laserDistanceDelta will hold  the distance the pod has traveled
  // 	since the laser sensor interupt last triggered.
  laserDistanceDelta += deltaPosition;

  // just used to slow things down for testing
  // delay(1000);
}

/*
 * Interrupt service routine for the counter
 *
 *  Waits for laserDelay amount of milliseconds and then increments the ticksSinceLastCheck when the counter detects a signal
 */
void counter_isr() {
  if(counterTime + COUNTER_DELAY < millis()) // pause for laserDelay number of millis after interrupt is triggered
  {
  	// TODO: after ensuring the delay is no longer needed remove it
    totalTicksCounter++; // increment number of ticks since the last check

    // increment pod distance be the didtance the pod travlels in one hall counter tick
    totalCounterDistance += COUNTER_TICK_DISTANCE;
    
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
  // ensures the pod has traveled far enough to not get a double reading from a reflective strip
  if(laserDistanceDelta > LASER_DELAY_DISTANCE) 
  {
    // increment number of ticks since the last check
    totalTicksLaser++;
    laserDistanceDelta = 0;

    // reset the counter distance based off strips which we assume to be accurate
    // TODO: we could add a check here to make sure we haven't missed a band
    totalCounterDistance = get_laser_position();
  }
}

/*
 * Sets up the interrupt for the counter
 */
void counter_setup()
{
  pinMode(counterSensorPin, INPUT_PULLUP);
  // TODO: determine if this should be FALLING RISING LOW or HIGH based on testing
  attachInterrupt(digitalPinToInterrupt(counterSensorPin), counter_isr, RISING); // trigger interrupt when signal from laser falls to 0
}

/*
 * Sets up the interrupt for the laser sensor
 */
void laser_setup()
{
  pinMode(laserSensorPin, INPUT_PULLUP);
  
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
  return totalCounterDistance;
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
      	Wire.write(velocity); // most recent instantaneous velocity

      } else if(request  == "ACCELERATION") {
      	Wire.write(acceleration); // most recent instantaneous acceleration

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
