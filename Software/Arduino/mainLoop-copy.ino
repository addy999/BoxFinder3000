#include <SoftwareSerial.h>
#include <string.h>

// Defines Motor pins
const int db = 13;
const int speedb = 11;
const int brakeb = 8;

const int da = 12;
const int speeda = 3;
const int brakea = 9;

const int dc = 6;
const int speedc = 7;
const int brakec = 5; 

const int motors[3][3] = {
    {da, brakea, speeda},
    {db, brakeb, speedb},
    {dc, brakec, speedc}
};

// defines Ultrasonic pin numbers
const int trigPin_1 = 22;
const int echoPin_1 = 23;

const int trigPin_2 = 24;
const int echoPin_2 = 25;

const int trigPin_3 = 26;
const int echoPin_3 = 27;

const int trigPin_4 = 28;
const int echoPin_4 = 29;

const int trigPin_5 = 30;
const int echoPin_5 = 31;

const int trigPin_6 = 32;
const int echoPin_6 = 33;

const int sensors[5][2] = {
    {trigPin_1, echoPin_1},
    {trigPin_2, echoPin_2},
    {trigPin_3, echoPin_3},
    {trigPin_4, echoPin_4},
    {trigPin_5, echoPin_5},
    // {trigPin_6, echoPin_6},
};

//  INitialize BT HC-06 Chip
// SoftwareSerial BTserial(50, 51); // RX | TX
const int LOOP_DELAY = 200; // ms

void setup() 
{
    // Initialize Sensor pins
    pinMode(trigPin_1, OUTPUT); 
    pinMode(echoPin_1, INPUT); 
    pinMode(trigPin_2, OUTPUT); 
    pinMode(echoPin_2, INPUT); 
    pinMode(trigPin_3, OUTPUT); 
    pinMode(echoPin_3, INPUT); 
    pinMode(trigPin_4, OUTPUT); 
    pinMode(echoPin_4, INPUT); 
    pinMode(trigPin_5, OUTPUT); 
    pinMode(echoPin_5, INPUT); 

    // Initialize Motor pins
    pinMode(db, OUTPUT);
    pinMode(speedb, OUTPUT);
    pinMode(brakeb, OUTPUT);
    pinMode(da, OUTPUT);
    pinMode(speeda, OUTPUT);
    pinMode(brakea, OUTPUT);
    pinMode(dc, OUTPUT);
    pinMode(speedc, OUTPUT);
    pinMode(brakec, OUTPUT);

    // Initialize Serial monitor
    Serial.begin(9600);
    Serial.println("Arduino is ready");

    // BTserial.begin(9600);     
}

void loop()
{   
    // Read sensors 
    float distances[6];
    for(int i=0; i<5; i++)
    {
        digitalWrite(sensors[i][0], LOW);
        delayMicroseconds(2);
        
        // Sets the trigPin on HIGH state for 10 micro seconds
        digitalWrite(sensors[i][0], HIGH);
        delayMicroseconds(10);
        digitalWrite(sensors[i][0], LOW);
        
        // Reads the echoPin, returns the sound wave travel time in microseconds
        float duration = pulseIn(sensors[i][1], HIGH);
        
        // Calculating the distance
        float distance = duration*0.034/2;

        // Convert dist to char and sent to BT
        char char_dist[10];
        dtostrf(distance, 6, 2, char_dist);
        Serial.print(char_dist);
        Serial.print("-");
    }
    Serial.print("\n");

    // Run motors
    digitalWrite(motors[0][0], LOW);
    digitalWrite(motors[0][1], LOW);
    analogWrite(motors[0][2], 255);

    digitalWrite(motors[1][0], LOW);
    digitalWrite(motors[1][1], LOW);
    analogWrite(motors[1][2], 255);

    digitalWrite(motors[2][0], LOW);
    digitalWrite(motors[2][1], LOW);
    analogWrite(motors[2][2], 255);

}