#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
#define NEOPIXEL_PIN 13
#define NUMPIXELS 40

Adafruit_NeoPixel pixels(NUMPIXELS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 20 

const int BUFFER_SIZE = 100;
char buf[BUFFER_SIZE];
// digital pin 2 has a pushbutton attached to it. Give it a name:
int pushButton = 7;
int incomingByte = 0;

String part01;
String part02;
String part03;
String part04;
String part05;

String part01_r;
String part01_g;
String part01_b;

String part02_r;
String part02_g;
String part02_b;

String part03_r;
String part03_g;
String part03_b;

String part04_r;
String part04_g;
String part04_b;

String part05_r;
String part05_g;
String part05_b;

int r1, g1, b1, r2, g2, b2, r3, g3, b3, r4, g4, b4, r5, g5, b5; 

//helper function to extract rgb value out of the string 
String getValue(String data, char separator, int index) {
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;
  
  for (int i=0; i<=maxIndex && found<=index; i++) {
    if (data.charAt(i) == separator || i==maxIndex) {
      found++;
      strIndex[0] = strIndex[1]+1;
      strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT);
  //start Neo pixel 
  pixels.begin();
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  int previousState; 
  int buttonState = digitalRead(pushButton);
  // print out the state of the button:
  if(previousState == 0 && buttonState == 1) {
    Serial.println(buttonState);  
  }
  if (Serial.available() >0) {
    String data = Serial.readStringUntil('\n'); //get data from PC
    part01 = getValue(data, ';', 0); // Split data into RGB value for the LED 
    part02 = getValue(data, ';', 1);
    part03 = getValue(data, ';', 2);
    part04 = getValue(data, ';', 3);
    part05 = getValue(data, ';', 4);
    part01_r = getValue(part01, ' ', 0);
    part01_g = getValue(part01, ' ', 1);
    part01_b = getValue(part01, ' ', 2);
    part02_r = getValue(part02, ' ', 0);
    part02_g = getValue(part02, ' ', 1);
    part02_b = getValue(part02, ' ', 2);
    part03_r = getValue(part03, ' ', 0);
    part03_g = getValue(part03, ' ', 1);
    part03_b = getValue(part03, ' ', 2);
    part04_r = getValue(part04, ' ', 0);
    part04_g = getValue(part04, ' ', 1);
    part04_b = getValue(part04, ' ', 2);
    part05_r = getValue(part05, ' ', 0);
    part05_g = getValue(part05, ' ', 1);
    part05_b = getValue(part05, ' ', 2);
    r1 = part01_r.toInt();
    g1 = part01_g.toInt();
    b1 = part01_b.toInt();
    r2 = part02_r.toInt();
    g2 = part02_g.toInt();
    b2 = part02_b.toInt();
    r3 = part03_r.toInt();
    g3 = part03_g.toInt();
    b3 = part03_b.toInt();
    r4 = part04_r.toInt();
    g4 = part04_g.toInt();
    b4 = part04_b.toInt();
    r5 = part05_r.toInt();
    g5 = part05_g.toInt();
    b5 = part05_b.toInt();
  }

    for (int i = 0; i <8; i++) {
      pixels.setPixelColor(i, pixels.Color(r1, g1, b1));
      delay(20);
      pixels.show();
    }
    for (int i = 8; i <16; i++) {
      pixels.setPixelColor(i, pixels.Color(r2, g2, b2));
      delay(20);
      pixels.show();
    }
    for (int i = 16; i <24; i++) {
      pixels.setPixelColor(i, pixels.Color(r3, g3, b3));  
      delay(20);
      pixels.show();
    }
    for (int i = 24; i <32; i++) {
      pixels.setPixelColor(i, pixels.Color(r4, g4, b4));
      delay(20);
      pixels.show();
    }
    for (int i = 32; i <40; i++) {
      pixels.setPixelColor(i, pixels.Color(r5, g5, b5));
      delay(20);
      pixels.show();
    }
    delay(200);
    pixels.clear();

    //printing function to know if the arduino get the correct rgb value 
//    Serial.print(part01);
//    Serial.print(" ");
//    Serial.print(part02);
//    Serial.print(" ");
//    Serial.print(part03);
//    Serial.print(" ");
//    Serial.print(part04);
//    Serial.print(" ");
//    Serial.println(part05);    

    previousState = buttonState;
    delay(500);        // delay in between reads for stability
}
