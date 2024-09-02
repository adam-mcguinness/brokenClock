class config:
    leds_per_tile = 3  # 3x3 tiles
    grid_cols = 7  # Width of the grid (7 columns as shown)
    grid_rows = 6  # Height of the grid (6 rows as shown)


def get_led_index(n):
    # Constants for the 3x3 LED tiles
    leds_per_tile_side = config.leds_per_tile
    print(f"leds_per_tile_side: {leds_per_tile_side}")
    leds_per_tile = leds_per_tile_side ** 2
    print(f"leds_per_tile: {leds_per_tile}")
    extra_cols = config.grid_cols % leds_per_tile_side
    print(f"extra_cols: {extra_cols}")
    tiles_per_row = config.grid_cols // leds_per_tile_side + extra_cols
    print(f"tiles_per_row: {tiles_per_row}")

    # Calculate overall LED position
    row = n // config.grid_cols  # Overall row
    print(f"row: {row}")
    col = n % config.grid_cols  # Overall column
    print(f"col: {col}")

    # Determine tile row and adjust column for snaking at the tile level
    tile_row = row // leds_per_tile_side
    print(f"tile_row: {tile_row}")
    tile_column = col // leds_per_tile_side
    print(f"tile_column: {tile_column}")

    extra_tile_cols = config.grid_cols // leds_per_tile_side

    # Adjust the within-tile column for snaking tiles in reverse rows

    # Assuming `extra_cols` is the number of columns in the last tile which might be different
    # And `extra_tile_cols` is not clearly used. It might be redundant or misnamed, review its necessity.

    # Calculate the linear index within the tile and overall index for full and partial tiles
    if extra_cols != 0 and tile_column == tiles_per_row - 1:
        if tile_row % 2 == 1:
            tile_linear_index = tile_row * tiles_per_row - 1 - tile_column + (tiles_per_row * tile_row)
        else:
            tile_linear_index = tile_row * tiles_per_row + tile_column

        within_tile_row = row % leds_per_tile_side
        within_tile_column = col % extra_cols
        index_in_tile = within_tile_row * extra_cols + within_tile_column

        print(f"LED is row {within_tile_row} in the tile")
        print(f"LED is col {within_tile_column} in the tile")
        print(f"index_in_tile: {index_in_tile}")
        print(f"tile_linear_index: {tile_linear_index}")

    else:
        within_tile_row = row % leds_per_tile_side
        within_tile_column = col % leds_per_tile_side
        index_in_tile = within_tile_row * leds_per_tile_side + within_tile_column
        tile_linear_index = tile_row * tiles_per_row + tile_column

    # Calculate the overall index
    if extra_cols != 0:
        leds_per_row_of_tiles = (config.grid_cols // leds_per_tile_side * leds_per_tile) + (extra_cols * leds_per_tile_side)
        leds_in_previous_rows = (tile_row * leds_per_row_of_tiles)
        overall_index = leds_in_previous_rows + (tile_column * leds_per_tile) + index_in_tile

    else:
        overall_index = tile_linear_index * leds_per_tile + index_in_tile

    return overall_index


index = [20, 27]
for index in index:
    led_index = get_led_index(index)
    print(f"LED at index {index} is the {led_index} led in the chain.")
