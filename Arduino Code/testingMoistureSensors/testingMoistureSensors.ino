const int AIR_VALUE = 3000;   // reading at air
const int WATER_VALUE = 1000; // reading at when soaked

void setup() {
  Serial.begin(9600);
  pinMode(36, INPUT);
}

void loop() {
  int val = constrain(analogRead(36), WATER_VALUE, AIR_VALUE);
  int moisture = map(val, AIR_VALUE, WATER_VALUE, 0, 100);
  Serial.println(moisture);
  delay(2000);

}
