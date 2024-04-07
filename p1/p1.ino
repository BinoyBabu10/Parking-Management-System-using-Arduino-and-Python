const int irSensorPin1 = 2; // IR sensor pin for slot 1
const int irSensorPin2 = 3; // IR sensor pin for slot 2
const int irSensorPin3 = 4; // IR sensor pin for slot 3

const int ledPin1 = 5; // LED pin for slot 1
const int ledPin2 = 6; // LED pin for slot 2
const int ledPin3 = 7; // LED pin for slot 3

void setup() {
  Serial.begin(9600);
  pinMode(irSensorPin1, INPUT);
  pinMode(irSensorPin2, INPUT);
  pinMode(irSensorPin3, INPUT);
  
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
}

void loop() {
  int slot1Status = digitalRead(irSensorPin1);
  int slot2Status = digitalRead(irSensorPin2);
  int slot3Status = digitalRead(irSensorPin3);

  digitalWrite(ledPin1, !slot1Status); // Invert status because IR sensor is active low
  digitalWrite(ledPin2, !slot2Status);
  digitalWrite(ledPin3, !slot3Status);

  Serial.print(slot1Status);
  Serial.print(slot2Status);
  Serial.println(slot3Status);

  delay(1000);
}
