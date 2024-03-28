import config
import ezdxf
import random
from drawDxf import calculate_clock_position
from clockFuntion import draw_clock

def get_led_index(n):
    # Constants for the 3x3 LED tiles
    leds_per_tile_side = 3
    leds_per_tile = leds_per_tile_side ** 2
    tiles_per_row = config.grid_cols // leds_per_tile_side

    # Calculate overall LED position
    r = n // config.grid_cols  # Overall row
    c = n % config.grid_cols  # Overall column

    # Determine tile row and adjust column for snaking at the tile level
    tile_row = r // leds_per_tile_side
    tile_column = c // leds_per_tile_side

    if tile_row % 2 == 1:  # Reverse direction for snaking rows
        tile_column = tiles_per_row - 1 - tile_column

    # Calculate position within the tile
    within_tile_row = r % leds_per_tile_side
    within_tile_column = c % leds_per_tile_side

    # Adjust the within-tile column for snaking tiles in reverse rows
    # No need to adjust within-tile positions since tiles themselves are not snaking internally

    # Calculate the linear index within the tile and overall index
    index_in_tile = within_tile_row * leds_per_tile_side + within_tile_column
    tile_linear_index = tile_row * tiles_per_row + tile_column
    overall_index = tile_linear_index * leds_per_tile + index_in_tile

    return overall_index

def main():
    doc = ezdxf.new('R2010')
    unit_codes = {
        "mm": 4,  # Millimeters
        "cm": 5,  # Centimeters
        "feet": 2,  # Feet
        "inches": 1  # Inches
    }
    doc.header['$INSUNITS'] = unit_codes[config.units.lower().strip()]
    msp = doc.modelspace()

    times = list(range(720))  # 720 minutes for 12 hours
    if config.randomize_clocks:
        random.shuffle(times)

    time_to_position = {}  # Dictionary to hold the time to position mapping

    for i, time in enumerate(times):
        hour = time // 60
        minute = time % 60
        row, col = divmod(i, config.grid_cols)
        center_x, center_y = calculate_clock_position(row, col)
        draw_clock(config.clock_style, (center_x, center_y), config.clock_diameter / 2, hour, minute,
                   msp)
        # Formatting time for 12-hour clock with AM/PM notation
        formatted_time = f"{hour % 12 if hour % 12 else 12}:{minute:02d}"
        time_to_position[formatted_time] = {"col": col, "row": row}

    # Save the DXF document
    doc.saveas("720_clocks.dxf")

    # Output the time to position mapping
    led_indices = [-1] * 720
    for time, pos in time_to_position.items():
        hour, minute = [int(x) for x in time.split(':')]
        minute_index = (hour % 12) * 60 + minute
        led_index = pos['row'] * config.grid_cols + pos['col']
        led_indices[minute_index] = led_index

    # output led indexes for arduino library.
    with open("./arduino/led_arrays.h", "w") as file:
        header = "#ifndef LED_ARRAYS\n#define LED_ARRAYS \n\n"
        footer = "\n#endif"
        file.write(header)
        file.write("const uint16_t ledMap[720] PROGMEM = {")
        for index in led_indices:
            file.write(f"  {index},")
        file.write("};\n")

        file.write("const uint16_t matrixMap[720] PROGMEM = {")
        lookup_table = [get_led_index(n) for n in range(720)]
        for index in lookup_table:
            file.write(f"  {index},")
        file.write("};\n")
        file.write(footer)

    # output mapping index in human-readable format.
    with open("720_clocks_index.txt", "w") as file:
        for time, pos in sorted(time_to_position.items(), key=lambda x: x[1]['row'] * config.grid_cols + x[1]['col']):
            file.write(f'"{time}": {{"col": {pos["col"]}, "row": {pos["row"]}}},\n')


if __name__ == "__main__":
    main()
