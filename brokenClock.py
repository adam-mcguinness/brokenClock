import config
import ezdxf
import random
from drawDxf import calculate_clock_position, draw_polyline_boarder
from clockFuntion import draw_clock


def get_led_index(n):
    # Grid configuration
    leds_per_tile_side = config.leds_per_tile
    total_cols = config.grid_cols
    total_rows = config.grid_rows
    extra_cols = total_cols % leds_per_tile_side
    extra_rows = total_rows % leds_per_tile_side

    # led configuration
    leds_per_standard_tile = leds_per_tile_side ** 2
    leds_per_supplemental_col_tile = 0
    if extra_cols > 0:
        leds_per_supplemental_col_tile = leds_per_tile_side * extra_cols
        # print(f"LEDs per Supplemental Row Tile: {leds_per_supplemental_row_tile}")
    if extra_rows > 0:
        leds_per_supplemental_row_tile = leds_per_tile_side * extra_rows

    # Calculate basic grid position
    led_grid_row = n // total_cols
    led_grid_col = n % total_cols
    # print(f"LED {n}: Position -> Row: {led_grid_row}, Column: {led_grid_col}")

    # Determine tiles per row
    standard_tiles_per_row = total_cols // leds_per_tile_side
    # print(f"Standard Tiles Per Row: {standard_tiles_per_row}")
    tiles_per_row = total_cols // leds_per_tile_side + (1 if total_cols % leds_per_tile_side > 0 else 0)

    # Determine tiles per column
    standard_tiles_per_col = total_rows // leds_per_tile_side
    tiles_per_col = total_rows // leds_per_tile_side + (1 if total_rows % leds_per_tile_side > 0 else 0)

    leds_per_tile_row = (leds_per_standard_tile * standard_tiles_per_row) + (
        leds_per_supplemental_col_tile if extra_cols != 0 else 0)
    # print(f"LEDs per Tile Row: {leds_per_tile_row}")

    # Determine the tile's row and column
    led_tile_row = led_grid_row // leds_per_tile_side
    led_tile_col = led_grid_col // leds_per_tile_side
    # print(f"Tile Position -> Row: {led_tile_row}, Column: {led_tile_col}")

    # Determine position within the tile
    if led_tile_col < tiles_per_row:
        # print("Standard Tile")
        within_tile_col = led_grid_col % leds_per_tile_side
    else:
        within_tile_col = led_grid_col % extra_rows

    if led_tile_row < tiles_per_col:
        # print("Standard Tile")
        within_tile_row = led_grid_row % leds_per_tile_side
    else:
        within_tile_row = led_grid_row % extra_cols
    # print(f"Within Tile Position -> Row: {within_tile_row}, Column: {within_tile_col}")

    if led_tile_col == (tiles_per_row - 1) and extra_cols != 0:
        # If this is the last column and it is a partial column
        index_in_tile = within_tile_col + within_tile_row * extra_cols
    else:
        index_in_tile = within_tile_row * leds_per_tile_side + within_tile_col
    # print(f"Index within Tile: {index_in_tile}")

    # calculate leds before current tile
    leds_in_rows_above = led_tile_row * leds_per_tile_row
    # print(f"LEDs in Rows Above: {leds_in_rows_above}")
    # reverse this for odd rows?

    leds_before_current_tile = leds_in_rows_above + (led_tile_col * leds_per_standard_tile)
    # print(f"LEDs Before Current Tile: {leds_before_current_tile}")
    if led_tile_row % 2 == 1:
        led_tile_col = (tiles_per_row - 1) - led_tile_col
        # print(f"Snaking Adjustment -> Column: {led_tile_col}")
        leds_before_current_tile = leds_in_rows_above + (led_tile_col * leds_per_supplemental_col_tile)
        if led_tile_col == tiles_per_row - 1 and extra_cols != 0:
            leds_before_current_tile = leds_in_rows_above + ((led_tile_col - 1) * leds_per_standard_tile) + leds_per_supplemental_col_tile

    # Calculate overall index
    overall_index = leds_before_current_tile + index_in_tile

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

    times = list(range(720))
    if config.randomize_clocks:
        random.shuffle(times)

    time_to_position = {}

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

    draw_polyline_boarder(msp)
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
