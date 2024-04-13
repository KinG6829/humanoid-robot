#include <Servo.h>

#define HEAD_SERVO_PIN 9
#define LEFT_LEG_MOTOR_PIN 10
#define RIGHT_LEG_MOTOR_PIN 11
#define LEFT_SONIC_TRIG_PIN 2
#define LEFT_SONIC_ECHO_PIN 3
#define RIGHT_SONIC_TRIG_PIN 4
#define RIGHT_SONIC_ECHO_PIN 5
#define IR_LEFT_PIN A0
#define IR_RIGHT_PIN A1
#define SONIC_TIMEOUT 30000 // Timeout in microseconds
#define SONIC_MAX_DISTANCE 200 // Maximum distance for sonic sensors in cm
#define IR_THRESHOLD 500 // Threshold for IR sensors
#define HEAD_ROTATION_ANGLE 45 // Angle for head rotation
#define LEG_FORWARD_SPEED 255 // Speed for forward movement
#define LEG_BACKWARD_SPEED 255 // Speed for backward movement
#define LEG_TURN_SPEED 200 // Speed for turning

Servo headServo;

void setup() {
  pinMode(LEFT_SONIC_TRIG_PIN, OUTPUT);
  pinMode(LEFT_SONIC_ECHO_PIN, INPUT);
  pinMode(RIGHT_SONIC_TRIG_PIN, OUTPUT);
  pinMode(RIGHT_SONIC_ECHO_PIN, INPUT);
  pinMode(IR_LEFT_PIN, INPUT);
  pinMode(IR_RIGHT_PIN, INPUT);
  pinMode(LEFT_LEG_MOTOR_PIN, OUTPUT);
  pinMode(RIGHT_LEG_MOTOR_PIN, OUTPUT);

  headServo.attach(HEAD_SERVO_PIN);
}

void loop() {
  if (detectObstacle()) {
    stopAndRotate();
  } else {
    moveForward();
  }
}

bool detectObstacle() {
  return (analogRead(IR_LEFT_PIN) > IR_THRESHOLD || analogRead(IR_RIGHT_PIN) > IR_THRESHOLD);
}

void stopAndRotate() {
  analogWrite(LEFT_LEG_MOTOR_PIN, 0);
  analogWrite(RIGHT_LEG_MOTOR_PIN, 0);

  headServo.write(90); // Move head to center
  delay(1000); // Wait for head to stabilize

  headServo.write(HEAD_ROTATION_ANGLE); // Rotate head to left
  delay(1000); // Adjust delay as needed

  if (!detectObstacle()) { // If no obstacle is detected after moving left
    headServo.write(90); // Return head to center
    delay(1000); // Wait for head to stabilize
    moveLeft(); // Move left as no obstacle is present
    return; // Exit the function
  }

  headServo.write(180); // Rotate head to right
  delay(2000); // Adjust delay as needed

  if (!detectObstacle()) { // If no obstacle is detected after moving right
    headServo.write(90); // Return head to center
    delay(1000); // Wait for head to stabilize
    moveRight(); // Move right as no obstacle is present
    return; // Exit the function
  }

  // If obstacles are detected in all directions
  moveBackward(); // Move backward
  delay(2000); // Adjust delay as needed
}

void moveForward() {
  analogWrite(LEFT_LEG_MOTOR_PIN, LEG_FORWARD_SPEED);
  analogWrite(RIGHT_LEG_MOTOR_PIN, LEG_FORWARD_SPEED);
}

void moveBackward() {
  analogWrite(LEFT_LEG_MOTOR_PIN, LEG_BACKWARD_SPEED);
  analogWrite(RIGHT_LEG_MOTOR_PIN, LEG_BACKWARD_SPEED);
}

void moveLeft() {
  analogWrite(LEFT_LEG_MOTOR_PIN, 0);
  analogWrite(RIGHT_LEG_MOTOR_PIN, LEG_TURN_SPEED);
}

void moveRight() {
  analogWrite(LEFT_LEG_MOTOR_PIN, LEG_TURN_SPEED);
  analogWrite(RIGHT_LEG_MOTOR_PIN, 0);
}

void stopMovement() {
  analogWrite(LEFT_LEG_MOTOR_PIN, 0);
  analogWrite(RIGHT_LEG_MOTOR_PIN, 0);
}

