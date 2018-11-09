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
