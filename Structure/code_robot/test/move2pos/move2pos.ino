#include <Servo.h>

Servo myservo;
float debut = 15;
float fin = 165;
char vitesse = 3; // de 1 à 5
float pos;
float length_angle;
float servo_pos;

void setup() {
  Serial.begin(9600);
  myservo.attach(2);

  length_angle = fin-debut;

  pos = debut;
}

void loop() {
  if (pos > fin)
    {pos = debut;}
  Serial.println(pos);
  
  myservo.write(pos);
  
  pos += length_angle/vitesse;
    
  delay(500);
}
