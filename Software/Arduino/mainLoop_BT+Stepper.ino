#include <string.h>
#include <Servo.h>

// // Initate Servo
// Servo name_servo;
// int servo_pos = 0;

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

const int sensors[6][2] = {
    {trigPin_1, echoPin_1},
    {trigPin_2, echoPin_2},
    {trigPin_3, echoPin_3},
    {trigPin_4, echoPin_4},
    {trigPin_5, echoPin_5},
    {trigPin_6, echoPin_6},
};

const int LOOP_DELAY = 50; // ms
float last_angle = -35; // deg

void setup() 
{   
    // Initialize servo
    // name_servo.attach(2);

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
    pinMode(trigPin_6, OUTPUT); 
    pinMode(echoPin_6, INPUT); 

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

        // Split command into [m1, m2, m3, angle, sleep]
        int first_comma_idx = bt_reading.indexOf(",");
        int fourth_comma_idx = bt_reading.lastIndexOf(",");
        int second_comma_idx = bt_reading.substring(first_comma_idx+1, fourth_comma_idx).indexOf(",") + first_comma_idx+1;
        int third_comma_idx = bt_reading.substring(first_comma_idx+1, fourth_comma_idx).lastIndexOf(",") + first_comma_idx+1;

        String m1_s = bt_reading.substring(0, first_comma_idx);
        String m2_s = bt_reading.substring(first_comma_idx+1, second_comma_idx);
        String m3_s = bt_reading.substring(second_comma_idx+1, third_comma_idx);
        String angle_s = bt_reading.substring(third_comma_idx+1, fourth_comma_idx);
        String sleep_s = bt_reading.substring(fourth_comma_idx+1, bt_reading.length()-1);

        // Convert commands into 3 floats
        float m1_f = m1_s.toFloat();
        float m2_f = m2_s.toFloat();
        float m3_f = m3_s.toFloat();
        float angle_f = angle_s.toFloat(); 
        float sleep_f = sleep_s.toFloat(); 
        float motor_commands[3] = {m1_f, m2_f, m3_f};
        
        // Operate
        if (angle_f==-1) {
            angle_f = last_angle;
        }
        // name_servo.write(angle_f);
        last_angle = angle_f;

        moveMotors(motor_commands);

        // Preview what's been sent
        Serial.print(m1_f);
        Serial.print(" ");
        Serial.print(m2_f);
        Serial.print(" ");
        Serial.print(m3_f);
        Serial.print(" ");
        Serial.print(angle_f);
        Serial.print("\n");

        delay(sleep_f);

        // Read Ultrasonic sensors 
        float distances[6];
        for(int i=0; i<6; i++)
        {
            for (int j=0; j<3; j++) 
            {
                digitalWrite(sensors[i][0], LOW);
                delayMicroseconds(2);
                // delay(100);
                
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
        }

        // End statement
        Serial1.print("\n");
    }
    
    // Brake after commands read and sensors sent back
    float commands[3] = {0.0, 0.0, 0.0};
    moveMotors(commands);
    delay(LOOP_DELAY);
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
            // analogWrite(speed_pin, 0);
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