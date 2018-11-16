/* Bryce Campbell
 * Monty Choy
 *
 * 11/3/18
 *
 * Last Updated - 11/5/18
 *
 * Code for laser sensor interrupt.
 */

#include <SoftwareSerial.h>

#define LASER_DELAY 1000 // wait this amount of time after each interupt
#define LASER_TICK_DISTANCE 100 // distance between reflective tape in feet

int laserSensorPin = 2; // pin for laser sensor interrupt

volatile double laserTime = millis(); // timer to prevent the interrupt from being called mulltiple times per strip.

volatile int totalTicks = 0; // the number of ticks the pod has traveled

int number = 0;

/*
 * Main loop
 */
void loop() {
  Serial.println(totalTicks); // print the total ticks for debug

  delay(1000);
}

void setup() {
  Serial.begin(9600); // start serial for output

  // initialize laser interupt
  laser_setup();

  Serial.println("Ready!");
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
    Serial.println("Interrupt");
    totalTicks++; // increment number of ticks since the last check
    laserTime = millis();
  }
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
  return totalTicks * LASER_TICK_DISTANCE;
}

/*
 * Temporary function repplace code and this comment when implemented
 */
int get_hall_position()
{
  return totalTicks * LASER_TICK_DISTANCE;
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
