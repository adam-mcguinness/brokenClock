# Broken Clock IRL

This is an attempt to bring a project by PierreMarTich to life in the real world. After seeing his absolutely "terrible" [project](https://www.reddit.com/r/badUIbattles/comments/r3q1tl/they_say_that_even_a_broken_clock_is_right_twice/) on [r/badUIbattles](https://www.reddit.com/r/badUIbattles/) I knew I needed one on my wall. 

You can find his original project [here](https://github.com/PierreMarTich/Broken_clock) and I must give him full credit for inspiring this idea.
# Code

## Image Generation
Wrote some trash python with a little help from ChatGPT and we are in business.

Vars you can play with:

| Variable Name                       | Type     | Default Value | Description                                                                              |
|-------------------------------------|----------|---------------|------------------------------------------------------------------------------------------|
| `style`                             | bool     | `False`       | Type of clock design. choose from `'standard'`, `'notch'`, `'cutout'`.                   |
| `clock_face`                        | bool     | `False`       | Enable drawing the clock face.                                                           |
| `clock_face_face_color`             | string   | `'none'`      | Not used currently.                                                                      |
| `clock_face_line_width`             | int      | `2`           | Line width of the clock face edge.                                                       |
| `add_quarter_hour_markers`          | bool     | `True`        | Enable drawing quarter-hour markers.                                                     |
| `quarter_hour_line_color`           | string   | `'white'`     | Not used currently.                                                                      |
| `quarter_hour_line_length`          | float    | `0.1`         | Length of the quarter-hour marker lines.                                                 |
| `quarter_hour_line_width`           | int      | `1`           | Line width of the quarter-hour markers.                                                  |
| `quarter_hour_line_offset`          | float    | `0.95`        | Offset from the center for quarter-hour markers.                                         |
| `add_5_minute_markers`              | bool     | `False`       | Enable drawing 5-minute markers.                                                         |
| `five_minute_color`                 | string   | `'white'`     | Not used currently.                                                                      |
| `five_minute_line_length`           | float    | `0.075`       | Length of the 5-minute marker lines.                                                     |
| `five_minute_line_width`            | float    | `0.5`         | Line width of the 5-minute markers.                                                      |
| `five_minute_line_offset`           | float    | `0.95`        | Offset from the center for 5-minute markers.                                             |
| `add_minute_markers`                | bool     | `False`       | Enable drawing 1-minute markers.                                                         |
| `minute_line_color`                 | string   | `'white'`     | Color of the minute markers.                                                             |
| `minute_line_length`                | float    | `0.05`        | Length of the minute marker lines.                                                       |
| `minute_line_width`                 | float    | `0.25`        | Line width of the minute markers.                                                        |
| `minute_line_offset`                | float    | `0.95`        | Offset from the center for minute markers.                                               |
| `hand_color`                        | string   | `'white'`     | Not used currently.                                                                      |
| `hour_hand_length`                  | float    | `0.5`         | Length of the hour hand.                                                                 |
| `hour_hand_width`                   | int      | `2`           | Width of the hour hand.                                                                  |
| `minute_hand_length`                | float    | `0.8`         | Length of the minute hand.                                                               |
| `minute_hand_width`                 | float    | `1.5`         | Width of the minute hand.                                                                |
| `units`                             | string   | `'mm'`        | Measurement units for layout and size. choose from `'inches'`, `'feet'`, `'cm'`, `'mm'`. |
| `grid_rows`, `grid_cols`            | int, int | `24, 30`      | Number of rows and columns in the grid layout.                                           |
| `clock_diameter`                    | int      | `30`          | Diameter of each clock.                                                                  |
| `spacing`                           | int      | `10`          | Spacing between clocks in the grid.                                                      |
| `outside_spacing`                   | int      | `20`          | Spacing between the dia. of the clock and the cut outline.                               |
| `background_color`                  | string   | `'black'`     | Not used currently.                                                                      |
| `randomize_clocks`                  | bool     | `False`       | Whether to randomize the positions of the clocks.                                        |
| `leds_per_tile`                     | int      | `3`           | Number of LEDs per tile in the mapping.                                                  |
| `width_in_tiles`, `height_in_tiles` | int, int | Calculated    | Width and height of the grid in tiles, calculated.                                       |

This also outputs the required vars and mapping to a .h file for importing to the microcontroller. After shuffling the clocks would be a major PITA to map manually.

Did alot of refactoring and now this outputs a dxf file directly for use with a plotter or laser cutter.

### **Fun Fact**: 
The chance of generating the same clock as someone else is ≈720! or greater than 1 in 2.60e1746. Meaning if you generated one every Planck time from the big bang until the heat death of the universe, you wouldn't even begin to scratch the surface of generating a duplicate. You would need another 10e1596 universe lengths to get there. 
## Arduino Sketch 
The main program is written in arduino for use with the attiny microcontroller. Main features included in the code are:
- saving and importing the LED mapping and Clock indexes from the library generated by the python code.
- 3 buttons for adjusting time with digital display utilizing the clock faces as digits.
  - hour increment button
  - minute increment button
  - second reset button

### Programing

As this is a tinyAVR 2-series, you can use the UPDI port to program the microcontroller with a single pin. There are a few things you need for this, but otherwise it is SUPER easy.
- Some sort of UART or TTL usb to serial connector. I bought [this](https://a.co/d/1Ms2zHJ) one, because usb-c.
- A 4.7kΩ resistor. It's talked about a lot more [here](https://github.com/SpenceKonde/AVR-Guidance/blob/master/UPDI/jtag2updi.md). Basically, I soldered the 4.7kΩ resistor to the TX and RX leads on the board and connected the RX to the UPDI port.  
- [megaTinyCore](https://github.com/SpenceKonde/megaTinyCore)
- Arduino IDE

Steps to flash:
1. Download and install the arduino IDE.
2. Install megaTinyCore, follow [these](https://github.com/SpenceKonde/megaTinyCore/blob/master/Installation.md#boards-manager-installation-now-strongly-recommended-unless-helping-with-core-development) steps.
3. Plug in usb adaptor and check Device Manager (for windows) to find the com port under ports.
4. Right-click on the com device, go to properties, port settings tab, advanced, change Latency Timer to 1.
5. Select your board in the IDE. Tools -> Board -> megaTinyCore -> "ATtiny3224/1624/1614/1604/824/814/804/424/414/404/214/204"
6. Select the com port for your usb adaptor. Tools -> Port -> "your com port from above"
7. Set the programmer this is what I used but might have to play around with it, [see docs](https://github.com/SpenceKonde/AVR-Guidance/blob/master/UPDI/jtag2updi.md#megatinycore). Tools -> Programmer -> "SerialUPDI - 230400 baud"
8. To program hook up the chip to VCC, GND, and the UPDI port to the RX on the programmer.
9. Verify the sketch, and make sure the generated .h file from the python script is in the same directory as the sketch.
10. Upload to the controller. If you are on a new arduino IDE v2 greater, you will need to use Sketch -> Upload Using Programmer.

# Hardware
## Electronics
### Microcontroller
The chosen microcontroller is an Attiny1624. This is the newer series 2 AVR from microchip. This has enough pins to interact with a RTC, 3 buttons for setting time, and control leads to address the LEDs for indicating.
### Real Time Clock
For the RTC I'm going with the accurate DS3231. It is extremely accurate and will only gain or lose about 1 minute a year. For all practical applications assuming you set your clock 2x a year for daylight savings the drift should be minimal. Especially for such an impractical piece of art.

This could also be subbed out for a DS1307 with minimal effort if the DS3231 is too pricey.
### LEDs
For the LEDs I have chosen to go with a 4000k individually addressable 5050 smd LED mounted to a 3x3 matrix pcb to allow tiling and cut down on the production costs while minimizing hand wiring.
## PCBs
### LED Matrix
This is a 3x3 tile that will be able to connect in a modular way to the ones adjacent to it for carry signal and power.

![PCB_matrix_v0.1.png](pcb%2Fled-matrix%2Fv0.1%2FPCB_matrix_v0.1.png)

Gerber files and schematics are available in the pcb folder.

This is v0.1 just ordered for testing. Will add a changelog here.

### Control Board
The control Board has all the other components to make this work microcontroller, RTC, buttons, etc.

![PCB_controller_v0.1.png](pcb%2Fcontroller%2Fv0.1%2FPCB_controller_v0.1.png)

Gerber files and schematics are available in the pcb folder.

This is v0.1 just ordered for testing. Will add a changelog here.
## Display

### Clocks
Still working out what would be best here. The running idea is to use a piece of glass or acrylic to hold a window cling or vinyl sticker for the clock faces. This should allow cheap manufacturing while providing the desired effect.
### Wall Mount/Bracket
Thinking about 3D printed parts to hold the LED Matrix boards, direct the light, and allow for modular connecting.


