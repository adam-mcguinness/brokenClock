# Broken Clock IRL

This is an attempt to bring a project by PierreMarTich to life in the real world. After seeing his absolutely terrible [project](https://www.reddit.com/r/badUIbattles/comments/r3q1tl/they_say_that_even_a_broken_clock_is_right_twice/) on [r/badUIbattles](https://www.reddit.com/r/badUIbattles/) I knew I needed one on my wall. 

You can find is original project [here](https://github.com/PierreMarTich/Broken_clock) and I must give him full credit for inspiring this idea.

## Code

### Image
Wrote some trash python with the help of a little chatgpt and we are in business.

**Fun Fact**: The chance of generating the same clock as someone else is ≈720! or greater than 1 in 2.60e1746.  
### arduino Sketch 
The main program is written in arduino for use with the attiny microcontroller. Main features included in the code are:
- Saving the index that is exported from the python image generation script to progmem to save ram.
- Mapping from the index to the tile-able 3x3 index.
- 3 buttons for adjusting time with digital display utilizing the clock faces as digits.
  - hour increment button
  - minuite increment button
  - second reset button
## Hardware

### Electronics
#### Microcontroller
The chosen microcontroller is an Attiny1624. This is the newer series 2 AVR from microchip. This has enough pins to interact with a RTC, 3 buttons for setting time, and control leads to address the LEDs for indicating.
#### Real Time Clock
For the RTC I'm going with the accurate DS3231. is will only gain or loose about 1 minute a year. For all practical applications assuming you set your clock 2x a year for daylight savings the drift should be minimal. Especially for such an impractical piece of art. 
#### LEDs
For the LEDs I have chose to go with a 4000k individually addressable 5050 smd LED mounted to a 3x3 matrix pcb to allow tiling and cut down on the production costs while minimizing hand wiring.
#### PCBs
LED Matrix will be a 3x3 tile that will be able to connect in a modular way to the ones adjacent to it for carry signal and power.

The control Board will house the microcontroller, rtc, usb-c power, and buttons for adjusting time.

### Materials



