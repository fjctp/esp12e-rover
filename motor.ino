#define MOTOR_SPD_L D1
#define MOTOR_SPD_R D2
#define MOTOR_DIR_L D3
#define MOTOR_DIR_R D4
#define PWM_BIT 8 // PWM resolution: 8, 10, 12, 16 bit at 1000 Hz
#define PWM_VAL_MAX pow(2, PWM_BIT)-1

void setup_motor(void) {
  // Set PWM resolution
  analogWriteResolution(PWM_BIT);

  // Setup pins
  pinMode(MOTOR_SPD_L, OUTPUT);
  pinMode(MOTOR_SPD_R, OUTPUT);
  pinMode(MOTOR_DIR_L, OUTPUT);
  pinMode(MOTOR_DIR_R, OUTPUT);
}

void update_motor(int valLeft, int valRight) {
  Serial.printf("Motor: %d, %d\n", valLeft, valRight);
.......................
  // Set direction
  digitalWrite(MOTOR_DIR_L, valLeft > 0 ? HIGH : LOW);
  digitalWrite(MOTOR_DIR_R, valRight > 0 ? HIGH : LOW);

  // Set speed
  analogWrite(MOTOR_SPD_L, map(abs(valLeft), 0, 127, 0, PWM_VAL_MAX));
  analogWrite(MOTOR_SPD_R, map(abs(valRight), 0, 127, 0, PWM_VAL_MAX));
}