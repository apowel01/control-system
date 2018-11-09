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
