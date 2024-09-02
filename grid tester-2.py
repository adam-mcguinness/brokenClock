class config:
    leds_per_tile = 3  # Assuming 3x3 tiles
    grid_cols = 7  # Width of the grid (7 columns)
    grid_rows = 9  # Height of the grid (6 rows)


def get_led_index(n):
    # Grid configuration
    leds_per_tile_side = config.leds_per_tile
    total_cols = config.grid_cols
    total_rows = config.grid_rows
    extra_cols = total_cols % leds_per_tile_side
    extra_rows = total_rows % leds_per_tile_side

    # led configuration
    leds_per_standard_tile = leds_per_tile_side ** 2
    # print(f"LEDs per Standard Tile: {leds_per_standard_tile}")
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


index_list = [42, 52, 62]
for idx in index_list:
    led_index = get_led_index(idx)
    print(f"LED at index {idx} is the {led_index} led in the chain.")
