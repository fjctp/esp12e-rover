#define LED_PIN LED_BUILTIN_AUX

unsigned long msToggle;
unsigned int ledState;

void setup_led(void) {
  pinMode(LED_PIN, OUTPUT);

  ledState = LOW;
  msToggle = 1e6; // Big number will result in a big `msDelta` that triggers an update.
}

void update_led(unsigned long msWait) {
  unsigned long msDelta = millis() - msToggle;
  if (msDelta > msWait) {
    msToggle = millis();
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState);
  }
}
