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

float readBT() 
{
    // Assume motors need to do nothing at first
    float motor_commands[3] = {NULL, NULL, NULL};
    

    return motor_commands
}