/*
  DigitalReadSerial

  Reads a digital input on pin 2, prints the result to the Serial Monitor

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/DigitalReadSerial
*/
const int BUFFER_SIZE = 50;
char buf[BUFFER_SIZE];
// digital pin 2 has a pushbutton attached to it. Give it a name:
int pushButton = 7;
int incomingByte = 0;
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  int buttonState = digitalRead(pushButton);
  // print out the state of the button:
//  Serial.print(buttonState);
  if (Serial.available() >0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
  }
  Serial.println(buttonState);
//  Serial.println("chao Vy ahihi");
  delay(50);        // delay in between reads for stability
}
