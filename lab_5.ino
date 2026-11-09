const int outputPin = 8;
const int inputPin = A0;

void setup() {
  Serial.begin(1000000); // Must match Python baud rate
  pinMode(outputPin, OUTPUT);
}

void loop() {
  tone(outputPin, 60); // 60 Hz square wave

    int val = analogRead(inputPin);
    Serial.print(millis());
    Serial.print(",");
    Serial.println(val);

}