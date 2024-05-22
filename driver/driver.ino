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
int canMove = 1;


// Serial Variables to control devices (servo or stepper)
int device = 0;
int value = 0;

char data[16];
char copyData[16];
char *token;


void calibrate() {
    // Stepper motor max speed and acceleration:
    stepper.setMaxSpeed(800);
    stepper.setAcceleration(100);

    while (digitalRead(homeButton)) {  // Move until the switch is activated   
        stepper.moveTo(initialHoming);  // Set the position to move to
        initialHoming++;  // Decrease by 1 for next move if needed
        stepper.run();  // Start moving the stepper
        delay(5);
    }

    stepper.setCurrentPosition(0);  // Set the current position as zero for now
    stepper.setMaxSpeed(800.0);
    stepper.setAcceleration(100.0);
    initialHoming = 1;

    while (!digitalRead(homeButton)) { // Move until the switch is deactivated
        stepper.moveTo(initialHoming);  
        stepper.run();
        initialHoming--;
        delay(5);
    }
    
    stepper.setCurrentPosition(0);
}


void setup() {
    // Serial communication
    Serial.begin(9600);
    while (!Serial) {
        // will wait until serial console opens
        delay(1);
    }
    Serial.println("Hello\n");

    // Endstop buttons
    pinMode(homeButton, INPUT_PULLUP);
    pinMode(maxButton, INPUT_PULLUP);
    delay(10);

    calibrate(); // Homing of stepper motor

    // Servo
    myservo.attach(servoPin);
    myservo.write(0);
}


void loop() {
    if (Serial.available() > 0) {
        String temp = Serial.readStringUntil('\n');
        temp.toCharArray(data, sizeof(data));
        // strcpy(copyData, data);

        token = strtok(data, ",");
        device = atoi(token);

        token = strtok(NULL, ",");
        value = atoi(token);

        // Received commands to move servo or the stepper, execute
        if (device == 1 && value >= 0) {
            // Move servo
            myservo.write(value);
        }
        else if (device == 2) { // && value > 0 && value < maxPosit
            // Move stepper motor
            stepper.setMaxSpeed(2000);
            stepper.setAcceleration(300);

          
            stepper.move(-value);
            stepper.runToPosition();

            // while (currPosit != value && digitalRead(maxButton)) {
            //     stepper.moveTo(currPosit);
            //     currPosit++;
            //     stepper.run();
            //     delay(5);
            // }

            // stepper.stop();
            // maxPosit = stepper.currentPosition();
        }
    }
}