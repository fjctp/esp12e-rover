#include <Servo.h>

#define MOTOR_SPD_L D1
#define MOTOR_SPD_R D2
#define MOTOR_DIR_L D3
#define MOTOR_DIR_R D4
#define LED_MS 250 // 0.25 sec
#define PWM_BIT 8 //8, 10, 12, 16 bit at 1000 Hz
#define PWM_VAL_MAX pow(2, PWM_BIT)-1

unsigned long msToggle;
unsigned int ledState;

void updateLed(unsigned int ms) {
  if ((millis() - msToggle) > ms) {
    msToggle = millis();
    ledState = !ledState;
    digitalWrite(LED_BUILTIN_AUX, ledState);
  }
}

void setup() {
  // LED
  pinMode(LED_BUILTIN_AUX, OUTPUT);
  ledState = HIGH;
  msToggle = millis();
  digitalWrite(LED_BUILTIN_AUX, ledState);

  // Motors
  analogWriteResolution(PWM_BIT);
  pinMode(MOTOR_SPD_L, OUTPUT);
  pinMode(MOTOR_SPD_R, OUTPUT);
  pinMode(MOTOR_DIR_L, OUTPUT);
  pinMode(MOTOR_DIR_R, OUTPUT);

  digitalWrite(MOTOR_DIR_L, HIGH);
  digitalWrite(MOTOR_DIR_R, HIGH);
}

void loop() {
  updateLed(LED_MS);
  
  analogWrite(MOTOR_SPD_L, map(80, 0, 100, 0, PWM_VAL_MAX));
  analogWrite(MOTOR_SPD_R, map(20, 0, 100, 0, PWM_VAL_MAX));
}
