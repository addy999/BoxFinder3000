
// Sharp IR GP2Y0A41SK0F Distance Test
// http://tinkcore.com/sharp-ir-gp2y0a41-skf/

#define sensor A0 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)

void setup() {
  Serial.begin(9600); // start the serial port
}

void loop() {
  
  // 5v
  float volts = analogRead(sensor);  // value from sensor * (5/1024)
  int distance = 12.08*pow(volts, -1.05); // worked out from datasheet graph
  Serial.println(distance); 
  delay(200); // slow down serial port 
}
