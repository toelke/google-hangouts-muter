#include <Bounce.h>

int led_nr = 1;
int btn_nr = 2;

static Bounce btn = Bounce(btn_nr, 10);

void setup() {
  pinMode(led_nr, OUTPUT);
  pinMode(btn_nr, INPUT_PULLUP);
  Serial.begin(9600);
}

static enum state {
  MUTE,
  UNMUTE,
  BLINKING
} s = BLINKING;

void loop() {
  if (btn.update()) {
    if (btn.fallingEdge()) {
      Serial.println(1);
    } else if (btn.risingEdge()) {
      Serial.println(0);
    }
  }

  if (Serial.available()) {
    char in = Serial.read();
    if (in == 'u') {
      s = UNMUTE;
      digitalWrite(led_nr, LOW);
    } else if (in == 'm') {
      s = MUTE;
      digitalWrite(led_nr, HIGH);
    } else if (in == '?') {
      s = BLINKING;
    }
  }

  if (s == BLINKING) {
    if (millis() % 1000 == 0) {
      digitalWrite(led_nr, HIGH);
    } else if (millis() % 1000 == 500) {
      digitalWrite(led_nr, LOW);
    }
  }
}
