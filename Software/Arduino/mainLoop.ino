#include <SoftwareSerial.h>

void setup() 
{
    //  INitialize BT HC-06 Chip
    SoftwareSerial BTserial(50, 3); // RX | TX
    BTserial.begin(9600); 

    // Initialize Serial monitor
    Serial.begin(9600);
    Serial.println("Arduino is ready");
}

void loop()
{
    motor_commands = readBT();
// - commands  = read latest Bluetooth readings, if avail

// - motors.applyCommand(command)
// - readings = sensors.read()

// - BT.send(readings)
}

float readBT(BTserial) 
{
    // Read BT Serial for motor commands

    // Assume motors need to do nothing at first
    float motor_commands[3] = {NULL, NULL, NULL};

    // Read BT
    char reading = "";
    if (BTserial.available())
    {  
        reading = BTserial.read();
        Serial.write("BT Command RX: ");
        Serial.write(reading);
    }
    if (reading[0] != '\0') {
        // Parse string
        motor_commands[0] = ;

        
    }
    return motor_commands
}