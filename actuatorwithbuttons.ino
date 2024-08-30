const int front = 14;
const int back = 12;//assign relay INx pin to arduino pin

void setup() {
  // put your setup code here, to run once:
  pinMode(16, INPUT_PULLUP);
  pinMode(17, INPUT_PULLUP);
  pinMode(front, OUTPUT);//set relay as an output
  pinMode(back, OUTPUT);//set relay as an output
  Serial.begin(9600);
}
void forwards() {
  digitalWrite(front, LOW); 
  digitalWrite(back, HIGH);
}

void backwards() {
  digitalWrite(front, HIGH);
  digitalWrite(back, LOW);
}

void stop(){
  digitalWrite(front, HIGH);
  digitalWrite(back, HIGH);
}

void loop() {
    if (digitalRead(16)==0) {
      backwards();
    }
    else if (digitalRead(17)==0) {
      forwards();
    }

    else {
      stop();
    }
}
