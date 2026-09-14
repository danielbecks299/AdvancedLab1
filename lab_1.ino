void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(A0);
  float v_out = sensorValue / 204.6;
  float v_in = 5;

  Serial.print(v_in, 4);
  Serial.print(" ");
  Serial.println(v_out, 4);

  delay(500);
}