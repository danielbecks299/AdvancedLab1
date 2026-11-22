void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  float v_out = sensorValue;
  // print out the value you read:
  Serial.print(millis());
  Serial.print(",");
  Serial.println(v_out);

  delay(100);  // delay in between reads for stability
}
