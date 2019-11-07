#include <stdio.h>
#include <math.h>
#include <Adafruit_NeoPixel.h>
#ifdef _AVR_
  #include <avr/power.h>
#endif

#define PIN 6 // pin LED connected to arduino
#define NUMPIXELS 32 // number of LEDs

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
//pixels.Color takes RGB values, from 0,0,0 up to 255,255,255

void setup(){
    Serial.begin(9600);
    pixels.begin(); //initialise pixel library
}

void pickedupblock(){
    for (i == 0, i < 5, i++){
        pixels.setPixelColor(i, pixels.Color(255,0,0));
    }
    pixels.setPixelColor(7,pixels.Color(255,0,0));
    pixels.setPixelColor(8,pixels.Color(255,0,0));
    pixels.setPixelColor(11,pixels.Color(255,0,0));
    pixels.setPixelColor(12,pixels.Color(255,0,0));
    pixels.setPixelColor(13,pixels.Color(255,0,0));
    pixels.setPixelColor(15,pixels.Color(255,0,0));
    pixels.setPixelColor(16,pixels.Color(255,0,0));
    pixels.setPixelColor(19,pixels.Color(255,0,0));
    pixels.setPixelColor(20,pixels.Color(255,0,0));
    for (i == 22, i < 29, i++){
        pixels.setPixelColor(i,pixels.Color(255,0,0));
    }
    pixels.setPixelColor(31,pixels.Color(255,0,0));
    pixels.show(); //updates pixel colours to the hardware
    delay(2000); //time LED shows
    for (i == 0, i < 32, i++){
        pixels.setPixelColor(i,pixels.Color(0,0,0));
    }
    pixels.show(); // all leds off
}

void droppedoffblock(){
    for (i == 0, i < 10, i++){
        pixels.setPixelColor(i, pixels.Color(255,0,0));
    }
    pixels.setPixelColor(11, pixels.Color(255,0,0));
    pixels.setPixelColor(12, pixels.Color(255,0,0));
    pixels.setPixelColor(16, pixels.Color(255,0,0));
    for (i == 19, i < 23, i++){
        pixels.setPixelColor(i, pixels.Color(255,0,0));
    }
    for (i == 24, i < 29, i++){
        pixels.setPixelColor(i, pixels.Color(255,0,0));
    }
    pixels.show(); //updates pixel colours to the hardware
    delay(2000); //time LED shows
    for (i == 0, i < 32, i++){
        pixels.setPixelColor(i, pixels.Color(0,0,0));
    }
    pixels.show(); //all LEDs off
}

//add to void loop
/*
location = variable //taken from addy's localisation
for (i == 0, i < 32, i++){
    pixels.setPixelColor(i, pixels.Color(0,0,0));
}
pixels.setPixelColor(variable,pixels.Color(0,255,0));
pixels.show(); //only one light remains on
*/
