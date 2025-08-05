/*
 * Main logic.
 */

#define LED_MS 250 // 0.25 sec
int valLeft = 0;
int valRight = 0;

void setup() {
  // Run once
  setup_ap();

  setup_led();
  setup_motor();
}

void loop() {
  // Run in a loop
  update_led(LED_MS);

  receive_msg(&valLeft, &valRight);
  update_motor(valLeft, valRight);
  delay(20);
}
