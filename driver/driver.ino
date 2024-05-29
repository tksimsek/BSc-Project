#include <Servo.h>
#include <SPI.h>
#include <Wire.h>
#include <AccelStepper.h>

#define stepPin 3
#define dirPin 2
#define motorInterfaceType 1

// Endstops
const int homeButton = 12;
const int maxButton = 11;


// AccelStepper instance
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);
long initialHoming = 1;  // Used to Home Stepper at startup
long currPosit = 1;


// Servo
Servo myservo;
int servoPin = 9;
int feedbackPin = A0;
int servo_position = 0;


// Serial Variables to control devices (servo or stepper)
int device = 0;
long value = 0;

char data[16];
char *token;


void calibrate() {
    // Stepper motor max speed and acceleration:
    stepper.setMaxSpeed(500);
    stepper.setAcceleration(100);

    while (digitalRead(homeButton)) {  // Move until the switch is activated   
        stepper.moveTo(initialHoming);  // Set the position to move to
        initialHoming += 2;  // Decrease by 1 for next move if needed
        stepper.run();  // Start moving the stepper
        delay(5);
    }

    stepper.setCurrentPosition(0);  // Set the current position as zero for now
    stepper.setMaxSpeed(500);
    stepper.setAcceleration(100.0);
    initialHoming = -1;

    while (!digitalRead(homeButton)) { // Move until the switch is deactivated
        stepper.moveTo(initialHoming);  
        stepper.run();
        initialHoming--;
        delay(5);
    }
    
    stepper.setCurrentPosition(0);
}


void move_servo(int target) {
  if (target > servo_position) {
    for (int i = servo_position; i < target; i += 4) {
      myservo.write(i);
      delay(50);
    }
    myservo.write(target);
    servo_position = target;
  }
  else if (target < servo_position) {
    for (int i = servo_position; i > target; i -= 4) {
      myservo.write(i);
      delay(50);
    }
    myservo.write(target);
    servo_position = target;
  }
}


void setup() {
    // Serial communication
    Serial.begin(9600);
    while (!Serial) {
        // will wait until serial comm opens
        delay(1);
    }
    Serial.print("driver_on\n");

    // Endstop buttons
    pinMode(homeButton, INPUT_PULLUP);
    pinMode(maxButton, INPUT_PULLUP);
    delay(10);

    // Servo
    myservo.attach(servoPin);
    myservo.write(servo_position);

    calibrate(); // Homing of stepper motor
    Serial.print("home\n");
}


void loop() {
    if (Serial.available() > 0) {
      if (!digitalRead(maxButton)) {
        calibrate();
      }
        String temp = Serial.readStringUntil('\n');
        temp.toCharArray(data, sizeof(data));

        token = strtok(data, ",");
        device = atoi(token);

        token = strtok(NULL, ",");
        value = atol(token);

        // Received commands to move servo or the stepper, execute
        if (device == 1 && value >= 0) {
            // Move servo
            move_servo(value);
            Serial.print("moved_s\n");
        }
        else if (device == 2 && value >= 0 && value <= 30000) { //  && value < maxPosit
            // Move stepper motor
            stepper.setMaxSpeed(800);
            stepper.setAcceleration(150);
          
            stepper.moveTo(-value);
            stepper.runToPosition();

            // while (stepper.currentPosition() != value) {
            //   stepper.run();
            // }
            Serial.print("moved_c\n");       
        }
    }
}