#include <Wire.h>
#include <SPI.h>
#include <avr/pgmspace.h>
#include <RTClib.h>
#include "led_arrays.h"

#define RTC_ADDRESS 0x68 // I2C address of the RTC
#define NUM_LEDS 720
#define WIDTH_IN_TILES 10
#define HEIGHT_IN_TILES 8

#define HOUR_BUTTON_PIN A6
#define MINUTE_BUTTON_PIN A5
#define SECOND_BUTTON_PIN A4

enum TimeUnit { HOURS, MINUTES, SECONDS };

// Timeout for Time Setting
const unsigned long timeoutDuration = 10000; 

RTC_DS3231 rtc;

bool lastHourButtonState = LOW;
bool lastMinuteButtonState = LOW;
bool lastSecondButtonState = LOW;
bool displayMode = false;

unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;
unsigned long lastModeSwitchTime = 0;

const uint16_t totalRows = 24;
const uint16_t totalColumns = 30;

const bool digitSegmentMap[10][7] = {
    {1, 1, 1, 1, 1, 1, 0}, // 0
    {0, 1, 1, 0, 0, 0, 0}, // 1
    {1, 1, 0, 1, 1, 0, 1}, // 2
    {1, 1, 1, 1, 0, 0, 1}, // 3
    {0, 1, 1, 0, 0, 1, 1}, // 4
    {1, 0, 1, 1, 0, 1, 1}, // 5
    {1, 0, 1, 1, 1, 1, 1}, // 6
    {1, 1, 1, 0, 0, 0, 0}, // 7
    {1, 1, 1, 1, 1, 1, 1}, // 8
    {1, 1, 1, 1, 0, 1, 1}  // 9
};

const uint16_t segmentIndexes[7][5] = {
    {0,1,2, 0xFFFF},       // A
    {2,32, 0xFFFF},        // B
    {62,92,122, 0xFFFF},   // C
    {120,121,122, 0xFFFF}, // D
    {60,90, 0xFFFF},       // E
    {0,30,0xFFFF},         // F
    {60,61,62, 0xFFFF}     // G
};

void setup() {

  SPI.begin();

  pinMode(HOUR_BUTTON_PIN, INPUT_PULLUP);
  pinMode(MINUTE_BUTTON_PIN, INPUT_PULLUP);
  pinMode(SECOND_BUTTON_PIN, INPUT_PULLUP);

  if (!rtc.begin()) {
    Serial.println("RTC failed");
  }
}

void loop() {
    unsigned long currentMillis = millis();

    // Handle button presses for mode switching and time adjustments
    if (digitalRead(HOUR_BUTTON_PIN) == LOW || digitalRead(MINUTE_BUTTON_PIN) == LOW || digitalRead(SECOND_BUTTON_PIN) == LOW) {
        if (currentMillis - lastDebounceTime > debounceDelay) {
            lastDebounceTime = currentMillis;
            lastModeSwitchTime = currentMillis; // Reset timeout timer
            displayMode = true; // Switch to display time mode
            
            // Adjust time based on which button was pressed
            if (digitalRead(HOUR_BUTTON_PIN) == LOW) adjustTime(HOURS);
            else if (digitalRead(MINUTE_BUTTON_PIN) == LOW) adjustTime(MINUTES);
            else if (digitalRead(SECOND_BUTTON_PIN) == LOW) adjustTime(SECONDS);
        }
    }

    // Display logic based on mode
    if (displayMode) {
        displayTime();
        if (currentMillis - lastModeSwitchTime > timeoutDuration) {
            displayMode = false; // Timeout reached, switch back to showing progress mode
        }
    } else {
        DateTime now = rtc.now();
        // Normalize the hour for a 12-hour format (0-11)
        uint8_t hour = now.twelveHour();
        // Calculate total minutes into the 12-hour cycle
        uint16_t minutesIntoCycle = hour * 60 + now.minute();
        // Ensure index wraps around correctly for a 12-hour cycle represented by 720 LEDs
        minutesIntoCycle = minutesIntoCycle % 720; // Ensures wrapping at the end of 12-hour cycle

        if (minutesIntoCycle < NUM_LEDS) {
            int ledIndex = getLedIndex(minutesIntoCycle);
            lightUpLED(ledIndex);
        } else {
            Serial.println("Error: Calculated LED index is out of range.");
        }
    }
}

void lightUpLED(uint16_t index) {
  startFrame();
  // LED Frames
  for (uint16_t i = 0; i < NUM_LEDS; i++) {
    if (i == index) {
      ledOn(1,255,255,255);
    } else {
      ledOff();
    }
  }
  endFrame();
}

void displayTime() {
    DateTime now = rtc.now();
    
    int hour = now.twelveHour();
    int hourTens = hour / 10;
    int hourOnes = hour % 10;
    int minuteTens = now.minute() / 10;
    int minuteOnes = now.minute() % 10;
    int secondTens = now.second() / 10;
    int secondOnes = now.second() % 10;
    
    // Starting indices calculation remains the same
    int digitsAndIndices[][2] = {
        {hourTens, 0},       // Hour tens
        {hourOnes, 4},       // Hour ones
        {minuteTens, 9},     // Minute tens
        {minuteOnes, 13},    // Minute ones
        {secondTens, 18},    // Second tens
        {secondOnes, 22}     // Second ones
    };

    lightUpDigits(digitsAndIndices, 6);
}

void lightUpDigits(const int digits[][2], int numDigits) {
  startFrame();
    
    // LED Frames
    for (uint16_t i = 0; i < NUM_LEDS; i++) {
        bool lightUp = false;
        for (int d = 0; d < numDigits; d++) {
            int digit = digits[d][0];
            uint16_t startIndex = digits[d][1];
            for (int segment = 0; segment < 7; segment++) {
                if (digitSegmentMap[digit][segment]) {
                    for (int j = 0; segmentIndexes[segment][j] != 0xFFFF; j++) {
                        uint16_t originalIndex = segmentIndexes[segment][j];
                        uint16_t adjustedIndex = getLedIndex(startIndex + originalIndex);
                        if (i == adjustedIndex) {
                            lightUp = true;
                            break;
                        }
                    }
                }
                if (lightUp) break;
            }
            if (lightUp) break;
        }
        
        if (lightUp) {
          ledOn(1,10,10,10);
        } else {
          ledOff();
        }
    }
  endFrame();
}


void adjustTime(TimeUnit unit) {
    DateTime now = rtc.now();
    int year = now.year();
    int month = now.month();
    int day = now.day();
    int hour = now.twelveHour();
    int minute = now.minute();
    int second = now.second();
    
    switch (unit) {
        case HOURS:
            hour = (hour + 1) % 24;
            break;
        case MINUTES:
            minute = (minute + 1) % 60;
            break;
        case SECONDS:
            second = 0; // Reset seconds to 0
            break;
    }
    rtc.adjust(DateTime(year, month, day, hour, minute, second));
}

void ledOn(uint8_t brightness, uint8_t red, uint8_t green, uint8_t blue){
  brightness = brightness & 0x1F;
  SPI.transfer(0XE0 | brightness);
  SPI.transfer(blue); // Blue
  SPI.transfer(green); // Green
  SPI.transfer(red); // Red
};

void ledOff(){
  SPI.transfer(0xE0 | 0x00);
  SPI.transfer(0x00);
  SPI.transfer(0x00);
  SPI.transfer(0x00);
};

void startFrame(){
  for (int i = 0; i < 4; i++) {
      SPI.transfer(0x00);
  }
};

void endFrame(){
    for (int i = 0; i < 4; i++) {
      SPI.transfer(0xFF);
  }
};

int getLedIndex(int n) {
    if (n >= 0 && n < NUM_LEDS) { // Assume NUM_LEDS is the total number of LEDs, replace with 720 if constant
        return pgm_read_word_near(matrixMap + n);
    } else {
        return -1; // Return an error code or handle the error as needed
    }
}
