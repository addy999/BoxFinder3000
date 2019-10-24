// Basic Bluetooth sketch BT_TALK
// Connect the module and communicate using the serial monitor
// Communicate with the BT module at 9600 (comms mode)
 
#include <SoftwareSerial.h>
SoftwareSerial BTserial(50, 3); // RX | TX
 
char c = ' ';
 
void setup() 
{
    Serial.begin(9600);
    Serial.println("Arduino is ready");
    Serial.println("Remember to select Both NL & CR in the serial monitor");
 
    // HC-05 default serial speed for Command mode is 9600
    BTserial.begin(9600);  
    BTserial.write("testing");
}
 
void loop()
{   

    // Keep reading from HC-05 and send to Arduino Serial Monitor
    if (BTserial.available())
    {  
        c = BTserial.read();
        Serial.write(c);
    }

    BTserial.write("Ayy lmao.\n");
//    delay(1000);

 
}
