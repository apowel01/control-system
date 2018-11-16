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

int breakTempuraturePins[] = {999, 999};

/*
 * Main loop
 */
void loop() {

  delay(1000);
}

void setup() {
  Serial.begin(9600); // start serial for output

  Serial.println("Ready!");
}

/*
 * returns the motor voltage of the input motor
 */
double get_motor_voltage(int motor_num) {
  return 999999999;
}

/*
 * returns the motor current of the input motor
 */
double get_motor_current(int motor_num) {
  return 999999999;
}

/*
 * returns the temurature on the given motor or -1 if the given motor is not in range
 * 
 * TODO: after sensor is speced out chance return to actual tempurature instead of placeholder.
 */
double get_break_tempurature(int breakPadNumber) {
	if(breakPadNumber < 0 || breakPadNumber >= (sizeof(breakTempuraturePins) / sizeof(int))) {
		Serial.println("Error in HealthMCU: breakPadNumber: " + (String)(breakPadNumber) + " out of allowed range: 0 - " + (String)(sizeof(breakTempuraturePins) / sizeof(int)));
   return -1; //if number out of allowed range return -1;
	}

  int breakPadPin = breakTempuraturePins[breakPadNumber]; //get pin

  double response = digitalRead(breakPadPin); //read on given pin

  return 999999999;

}

/*
 * return temperature of given motor
 * Does sensor refer to a pin? 
 * What is the relationship between sensor and motor in terms of data?
 */
int get_motor_heat (int sensor, int motor) {
	return 1000;
}
