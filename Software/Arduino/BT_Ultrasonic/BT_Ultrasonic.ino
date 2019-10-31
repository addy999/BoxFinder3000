#include <SoftwareSerial.h>
#include <stdio.h>
#include <string.h>
SoftwareSerial BTserial(50, 3); // RX | TX

// defines pins numbers
const int trigPin_1 = 9;
const int echoPin_1 = 10;
const int trigPin_2 = 11;
const int echoPin_2 = 12;
const int trigPin_3 = 4;
const int echoPin_3 = 5;

// defines variables

int distanceVector[2];

long duration_1;
int distance_1;
long duration_2;
int distance_2;
 
char c = ' ';
float triggers[3] = {trigPin_1, trigPin_2, trigPin_3};
float echos[3] = {echoPin_1, echoPin_2, echoPin_3};
 
void setup() 
{
    Serial.begin(9600);
    Serial.println("Arduino is ready");
    Serial.println("Remember to select Both NL & CR in the serial monitor");

    pinMode(trigPin_1, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin_1, INPUT); // Sets the echoPin as an Input
    pinMode(trigPin_2, OUTPUT); 
    pinMode(echoPin_2, INPUT); 
    pinMode(trigPin_3, OUTPUT); 
    pinMode(echoPin_3, INPUT); 
 
    // HC-05 default serial speed for Command mode is 9600
    BTserial.begin(9600);  
    BTserial.write("Testing");
}
 
void loop()
{   
    // Serial.print("Loop starting\n");

    float distances[3];

    for(int i =0; i<3; i++)
    {
        // Serial.print(i);

        digitalWrite(triggers[i], LOW);
        delayMicroseconds(2);
        
        // Sets the trigPin on HIGH state for 10 micro seconds
        digitalWrite(triggers[i], HIGH);
        delayMicroseconds(10);
        digitalWrite(triggers[i], LOW);
        
        // Reads the echoPin, returns the sound wave travel time in microseconds
        float duration = pulseIn(echos[i], HIGH);
        
        // Calculating the distance
        float distance = duration*0.034/2;
        distances[i] = distance;

    }

    // // Keep reading from HC-05 and send to Arduino Serial Monitor
    // if (BTserial.available())
    // {  
    //     c = BTserial.read();
    //     Serial.write(c);
    // }

    // Serial.print("Let's split arrays\n");
    char dist1[10], dist2[10], dist3[10];
    dtostrf(distances[0], 6, 2, dist1);
    dtostrf(distances[1], 6, 2, dist2);
    dtostrf(distances[2], 6, 2, dist3);

    // Serial.print(dist1);
    // Serial.print(" ");
    // Serial.print(dist2);
    // Serial.print(" ");
    // Serial.print(dist3);
    // Serial.print("\n");

    Serial.print("Let's concat\n");
    char concat_dist[sizeof(dist1)+sizeof(dist2)+sizeof(dist3)+2] = "";
    strcat(concat_dist, dist1);
    strcat(concat_dist, "-");
    strcat(concat_dist, dist2);
    strcat(concat_dist, "-");
    strcat(concat_dist, dist3);
    
    Serial.print("\n Concat dist: \n");
    Serial.print(concat_dist);
    Serial.print("\n");

    BTserial.write("Incoming readings: ");
    BTserial.write(concat_dist);
    BTserial.write("\n");
    delay(1000);
 
}
