#include <SoftwareSerial.h>
SoftwareSerial BTserial(50, 3); // RX | TX

// defines pins numbers
const int trigPin_1 = 9;
const int echoPin_1 = 10;
const int trigPin_2 = 11;
const int echoPin_2 = 12;

// defines variables

int distanceVector[2];

long duration_1;
int distance_1;
long duration_2;
int distance_2;
 
char c = ' ';
 
void setup() 
{
    Serial.begin(9600);
    Serial.println("Arduino is ready");
    Serial.println("Remember to select Both NL & CR in the serial monitor");

    pinMode(trigPin_1, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin_1, INPUT); // Sets the echoPin as an Input
    pinMode(trigPin_2, OUTPUT); 
    pinMode(echoPin_2, INPUT); 
 
    // HC-05 default serial speed for Command mode is 9600
    BTserial.begin(9600);  
    BTserial.write("testing");
}
 
void loop()
{   
    digitalWrite(trigPin_1, LOW);
    digitalWrite(trigPin_2, LOW);
    delayMicroseconds(2);
    
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin_1, HIGH);
    digitalWrite(trigPin_2, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin_1, LOW);
    digitalWrite(trigPin_2, LOW);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration_1 = pulseIn(echoPin_1, HIGH);
    duration_2 = pulseIn(echoPin_2, HIGH);
    
    // Calculating the distance
    distance_1 = duration_1*0.034/2;
    distance_2 = duration_2*0.034/2;
    
    // Keep reading from HC-05 and send to Arduino Serial Monitor
    if (BTserial.available())
    {  
        c = BTserial.read();
        Serial.write(c);
    }

    //distanceVector[0] = distance_1;
    //distanceVector[1] = distance_2;

    BTserial.write("Incoming readings: \n");
    BTserial.write(distance_1);
    BTserial.write("\t");
    BTserial.write(distance_2);
    BTserial.write("\t");
//    delay(1000);

 
}
