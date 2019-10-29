#include <stdio.h>
#include <math.h>

int wheel_1 = 11 //front left wheels: positive forward
int wheel_2 = 12 //front right: positive forward
int wheel_3 = 13 // back: positve rotate to the left of the robot

void setup(){
    Serial.begin(9600);
}

void loop(){
    int sen_array[5]
    sen_array[0] = analogRead(A0); // 0 - 255 F
    sen_array[1] = analogRead(A1); // L
    sen_array[2] = analogRead(A2); // B not needed for avoidance
    sen_array[3] = analogRead(A3); // R
    sen_array[4] = analogRead(A4); // FL
    sen_array[5] = analogRead(A5); // FR
    
    for (i == 0, i < 6, i++){ // Front Sensor
        Serial.println(sen_array[i]); //print value to serial
        if (sen_array[i] <= 100){ // replace 100 with actual measurement
            if (i == 0){
                analogWrite(wheel_1, 255); //fine tune and idk how to the H-bridge
                analogWrite(wheel_2, -255);
                analogWrite(wheel_3, 255); // robot rotates clockwise
                delay (100); //use this to fine tune to 90 deg clockwise
            }
            if (i == 1){ //Right Sensor
                if (sen_array[5] < 141){ // check if robot is facing towards (pythagoras)
                    analogWrite(wheel_1, -255); //fine tune and idk how to the H-bridge
                    analogWrite(wheel_2, 255);
                    analogWrite(wheel_3, -255); // robot rotates anti-clockwise
                    delay (100); //fine tune to x degrees
                }
            }
            if (i == 3){ //Left Sensor
                if (sen_array[4] < 141){ // check if robot is facing towards (pythagoras)
                    analogWrite(wheel_1, 255); //fine tune and idk how to the H-bridge
                    analogWrite(wheel_2, -255);
                    analogWrite(wheel_3, 255); // robot rotates clockwise
                    delay (100); //fine tune to x degrees
                }
            }
            if (i == 4){ //Front Left Sensor
                analogWrite(wheel_1, 255);
                analogWrite(wheel_2, -255);
                analogWrite(wheel_3, 255); // robot rotates clockwise ()
                delay(100); //fine tune to x degrees
                
            }
            if (i == 5){ //Front Right Sensor
                analogWrite(wheel_1, -255);
                analogWrite(wheel_2, 255);
                analogWrite(wheel_3, -255); // robot rotates anti-clockwise ()
                delay(100); //fine tune to x degrees
                analogWrite(wheel_1, 0); 
                analogWrite(wheel_2, 0);
                analogWrite(wheel_3, 0);
            }
        analogWrite(wheel_1, 0);
        analogWrite(wheel_2, 0);
        analogWrite(wheel_3, 0); // stops robot
        }
    }

    return 0;
}