int db = 13;
int speedb = 11;
int brakeb = 8;


void setup() {
  // put your setup code here, to run once:

  pinMode(db, OUTPUT);
  pinMode(speedb, OUTPUT);
  pinMode(brakeb, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

  digitalWrite(db, HIGH);
  digitalWrite(brakeb, LOW);
  analogWrite(speedb, 255);
  

}
