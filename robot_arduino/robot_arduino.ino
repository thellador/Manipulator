#define AMOUNT 6

#include <AsyncStream.h>
AsyncStream<100> serial(&Serial, '\n');

#include <GParser.h>
#include <ServoSmooth.h>
ServoSmooth servos[AMOUNT];

uint32_t servoTimer;

void setup() {
  Serial.begin(115200);

  servos[0].setAutoDetach(false);
  servos[1].setAutoDetach(false);
  servos[2].setAutoDetach(false);
  servos[3].setAutoDetach(false);
  servos[4].setAutoDetach(false);
  servos[5].setAutoDetach(false);

  servos[0].attach(2, 500, 2500);
  servos[1].attach(3, 500, 2500);
  servos[2].attach(4, 500, 2500);
  servos[3].attach(5, 350, 2350);
  servos[4].attach(6, 500, 2500);
  servos[5].attach(7, 500, 2500);

  servos[0].setSpeed(180);
  servos[0].setAccel(0.1);
  servos[1].setSpeed(300);
  servos[1].setAccel(0.2);
  servos[2].setSpeed(180);
  servos[2].setAccel(0.1);
  servos[3].setSpeed(180);
  servos[3].setAccel(0.1);
  servos[4].setSpeed(400);
  servos[4].setAccel(0.2);
  servos[5].setSpeed(180);
  servos[5].setAccel(0.1);

  servos[0].setTargetDeg(75);
  servos[1].setTargetDeg(90);
  servos[2].setTargetDeg(90);
  servos[3].setTargetDeg(92);
  servos[4].setTargetDeg(90);
  servos[5].setTargetDeg(95);
}

void loop() {
  if (millis() - servoTimer >= 20) {
    servoTimer += 20;
    for (byte i = 0; i < AMOUNT; i++) {
      servos[i].tickManual();
    }
  }

  if (serial.available()) {
    GParser data(serial.buf, ' ');
    int am = data.split();

    if (am == 6) {
      int angle6 = data.getInt(0);
      int angle5 = data.getInt(1);
      int angle4 = data.getInt(2);
      int angle3 = data.getInt(3);
      int angle2 = data.getInt(4);
      int angle1 = data.getInt(5);

      servos[0].setTargetDeg(angle1);
      servos[1].setTargetDeg(angle2);
      servos[2].setTargetDeg(angle3);
      servos[3].setTargetDeg(angle4);
      servos[4].setTargetDeg(angle5);
      servos[5].setTargetDeg(angle6);
    } else {
      Serial.println("Error: Expected 6 angles");
    }
  }
}
