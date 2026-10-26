/*
CCNY PHYS 37100
Experiment 4b
More accurate timings
*/
float currentTime = 0.0;
float lastTime = 0.0;
// CHANGED: Increased to 1000000 for a 1-second interval (1,000,000 microseconds)
const unsigned long intervalBetweenData = 10000; 

void setup() {
  // Make the serial talk faster
  // Be sure to also change this in the serial monitor window settings!
  Serial.begin(2000000);
}

void loop() {
  // Get the current time in microseconds
  currentTime = micros();
  
  if (currentTime - lastTime >= intervalBetweenData) {
    int sensorValue = analogRead(A0);
    lastTime += intervalBetweenData;
    
    // Prints time in milliseconds, then the sensor data
    Serial.print(currentTime/1000000); 
    Serial.print(',');
    Serial.println(sensorValue);
  }
}
