char* x;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);
}

void  loop() {
  while (!Serial.available());
  x = Serial.readString();
  Serial.print(99);
  
}