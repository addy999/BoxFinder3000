int db = 13;
int speedb = 11;
int brakeb = 8;

int da = 12;
int speeda = 3;
int brakea = 9;

int dc = 6;
int speedc = 7;
int brakec = 5; 


void setup() {
  // put your setup code here, to run once:

  pinMode(db, OUTPUT);
  pinMode(speedb, OUTPUT);
  pinMode(brakeb, OUTPUT);

  pinMode(da, OUTPUT);
  pinMode(speeda, OUTPUT);
  pinMode(brakea, OUTPUT);

  pinMode(dc, OUTPUT);
  pinMode(speedc, OUTPUT);
  pinMode(brakec, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

  digitalWrite(db, HIGH);
  digitalWrite(brakeb, LOW);
  analogWrite(speedb, 255);

  digitalWrite(da, HIGH);
  digitalWrite(brakea, LOW);
  analogWrite(speeda, 255);

  digitalWrite(dc, HIGH);
  digitalWrite(brakec, LOW);
  analogWrite(speedc, 255);
  

}
