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

    Serial1.begin(9600);
    Serial1.println("BT WORKING");
    
}

void loop()
{   
    if (Serial1.available())
    {   
        // Read BT and move motor 

        String bt_reading;
        bt_reading = Serial1.readStringUntil("\n");
//        Serial.print(bt_reading); // Preview sent command

        // Split command into 3 strings
        int first_comma_idx = bt_reading.indexOf(",");
        int last_comma_idx = bt_reading.lastIndexOf(",");
        int hyphen_idx = bt_reading.lastIndexOf("-");
        String m1_s = bt_reading.substring(0, first_comma_idx);
        String m2_s = bt_reading.substring(first_comma_idx+1, last_comma_idx);
        String m3_s = bt_reading.substring(last_comma_idx+1, hyphen_idx);
        String sleep_s = bt_reading.substring(hyphen_idx+1, bt_reading.length()-1);

        // Convert commands into 3 floats
        float m1_f = m1_s.toFloat();
        float m2_f = m2_s.toFloat();
        float m3_f = m3_s.toFloat();
        float sleep_f = sleep_s.toFloat(); 
        float motor_commands[3] = {m1_f, m2_f, m3_f};
        moveMotors(motor_commands);

        Serial.print(m1_f);
        Serial.print(m2_f);
        Serial.print(m3_f);
//        Serial.print(sleep_f);
        Serial.print("\n");

        delay(sleep_f);

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
            Serial1.print(char_dist);
            Serial1.print("-");
        }
        Serial1.print("\n");
    }
    
    float commands[3] = {0.0, 0.0, 0.0};
    moveMotors(commands);
    delay(50);
}

char distToChar(float* distances)
{
    char concat_dist[sizeof(distances) * 10 + sizeof(distances)] = "";

    for(int i=0; i<sizeof(distances); i++)
    {
        char char_dist[10];
        dtostrf(distances[i], 6, 2, char_dist);
        strcat(concat_dist, char_dist);
        strcat(concat_dist, "-");
    }

    return concat_dist;
}

void moveMotors(float motor_commands[3])
{
    for(int i=0; i<3; i++)
    {
        int direction_pin = motors[i][0];
        int brake_pin = motors[i][1];
        int speed_pin = motors[i][2];
        float given_command = motor_commands[i];

        if (given_command == 0) 
        {
            digitalWrite(brake_pin, HIGH);
            // delay(100);
            // digitalWrite(brake_pin, LOW);
        }
        else if (given_command < 0)
        {
            digitalWrite(brake_pin, LOW);
            digitalWrite(direction_pin, LOW);
            analogWrite(speed_pin, given_command * -1);
        }
        else 
        {
            digitalWrite(brake_pin, LOW);
            digitalWrite(direction_pin, HIGH);
            analogWrite(speed_pin, given_command);
        }
    }
}