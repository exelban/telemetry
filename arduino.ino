#include <SimpleTimer.h>

float temperatura1, temperatura2, temperatura3, R, U, I, V;
boolean speed_value = false;
unsigned long time_for_calculation;
float wheel = 0.87;
SimpleTimer timerForSendData;

void setup() {
  Serial.begin(9600);

  timerForSendData.setInterval(50, sendData);
  attachInterrupt(digitalPinToInterrupt(2), get_speed, LOW);
}

void loop() {
  get_temperature1();
  get_temperature2();
  get_temperature3();
  get_U();
  get_I();

  timerForSendData.run();
}


void sendData() {
  String data = String(U) + " " +
                String(I) + " " +
                String(temperatura1) + " " +
                String(temperatura2) + " " +
                String(temperatura3) + " " +
                String(V);

  Serial.println(String(data));
}

void get_temperature1() {
  temperatura1 = analogRead(A4);
  R = ((10240000 / temperatura1) - 10000);
  temperatura1 = (1 / (0.001129148 + (0.000234125 * (log(R))) + (0.0000000876741 * (log(R) * log(R) * log(R))))) - 273.15;
}
void get_temperature2() {
  temperatura2 = analogRead(A3);
  R = ((10240000 / temperatura2) - 10000);
  temperatura2 = (1 / (0.001129148 + (0.000234125 * (log(R))) + (0.0000000876741 * (log(R) * log(R) * log(R))))) - 273.15;
}
void get_temperature3() {
  temperatura3 = analogRead(A2);
  R = ((10240000 / temperatura3) - 10000);
  temperatura3 = (1 / (0.001129148 + (0.000234125 * (log(R))) + (0.0000000876741 * (log(R) * log(R) * log(R))))) - 273.15;
}
void get_U() {
  U = ((analogRead(A1) - 515) * 0.5818);
}
void get_I() {
  I = (((int(analogRead(A0)) * 0.1) * 55) / 1024) * 10;
}
void get_speed() {
  if (speed_value == false) {
    detachInterrupt(digitalPinToInterrupt(2));
    speed_value = true;
    time_for_calculation = millis();
    attachInterrupt(digitalPinToInterrupt(2), get_speed, HIGH);
  }
  else {
    detachInterrupt(digitalPinToInterrupt(2));
    speed_value = false;
    time_for_calculation = millis() - time_for_calculation;
    V = (wheel / time_for_calculation * 10) * 36;
    attachInterrupt(digitalPinToInterrupt(2), get_speed, HIGH);
  }
}
