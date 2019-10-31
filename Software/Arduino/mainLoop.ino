#include <SoftwareSerial.h>

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
}

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

const int LOOP_DELAY = 500; // ms

void setup() 
{
    //  INitialize BT HC-06 Chip
    SoftwareSerial BTserial(50, 3); // RX | TX
    BTserial.begin(9600); 

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
    
}

void loop()
{   
    if (BTserial.available())
    {
        char command = BTserial.read();
        Serial.write(command); // Preview sent command
        float motor_commands[3] = parseMotorCommand(command);
        moveMotors(motor_commands);
    }
    
    float readings[6] = readSensors(sensors);
    sendToBT(readings);
    delay(LOOP_DELAY);
}


float readSensors(sensors)
{
    float distances[6];

    for(int i=0; i<6; i++)
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
        distances[i] = distance;
    }

    return distances;
}

char distToChar(distances)
{
    char concat_dist[sizeof(distances) * 10 + sizeof(distances)] = "";

    for(int i =0; i<sizeof(distances); i++)
    {
        char char_dist[10];
        dtostrf(distances[i], 6, 2, char_dist);
        strcat(concat_dist, char_dist);
        strcat(concat_dist, "-");
    }

    return concat_dist;
}

void sendToBT(BTserial, readings)
{
    // Convert sensor distance readings to char array 
    char char_array = distToChar(readings);

    // Send to BT
    BTserial.write("Incoming readings: ");
    BTserial.write(char_array);
    BTserial.write("\n");
}

void moveMotors(motor_commands)
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

float parseMotorCommand(command) 
{
    // Read BT Serial for motor commands

    // Assume motors need to do nothing at first
    float motor_commands[3] = {NULL, NULL, NULL};

    // Read BT
    
    if (reading[0] != '\0') {
        // Parse string
        motor_commands[0] = ;

        
    }
    return motor_commands
}