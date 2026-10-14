const int thermPin = A0; 
const int potPin = A1; 
const int outPin = 9; 

int thermValue = 0;
int potValue = 0;
int outputLevel = 0;

// Voltage divider fixed resistor (1k ohms)
const float R1 = 1000.0; 

// Thermistor constants
const float BETA = 3950.0;       
const float R0 = 3300.0;       // 3.3k ohms at 25 °C
const float T0 = 298.15;       // 25 °C in Kelvin

float Rt;

void setup() {
    pinMode(outPin, OUTPUT);
    Serial.begin(9600);
    Serial.println("Time_s,Potentiometer,ThermistorRaw");
}

void loop() {
    potValue = analogRead(potPin);
    thermValue = analogRead(thermPin);
    
    outputLevel = potValue / 4;
    analogWrite(outPin, outputLevel);

    Serial.print(float(millis())/1000);
    Serial.print(",");
    Serial.print(potValue);
    Serial.print(",");
    Serial.print(outputLevel);
    Serial.print(",");
    Serial.print(thermValue);
    
    delay(200);
}