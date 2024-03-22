import matplotlib.pyplot as plt
import numpy as np
import random

from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Polygon

# Clock Face and Sizing
clock_face = False
clock_face_edge_color = 'white'
clock_face_face_color = 'none'
clock_face_line_width = 2

# Quarter Hour Markers
add_quarter_hour_markers = True
quarter_hour_line_color = 'black'
quarter_hour_line_length = 0.1
quarter_hour_line_width = 0.25
quarter_hour_line_offset = 0.95

# 5 Minute Markers
add_5_minute_markers = True
five_minute_color = 'black'
five_minute_line_length = 0.075
five_minute_line_width = 0.01
five_minute_line_offset = 0.95

# 1 Minute Markers
add_minute_markers = False
minute_line_color = 'white'
minute_line_length = 0.05
minute_line_width = 0.25
minute_line_offset = 0.95

# Hands
hand_color = 'black'
hour_hand_length = 0.5
hour_hand_width = 0.25
minute_hand_length = 0.8
minute_hand_width = 0.01

# Layout and Size
units = 'mm'  # options are inches, cm, mm, feet, and meters
grid_rows, grid_cols = 24, 30
clock_diameter = 30
spacing = 10
background_color = 'none'
randomize_clocks = False

# Tiles for Mapping
leds_per_tile = 3
width_in_tiles = grid_cols // leds_per_tile
height_in_tiles = grid_rows // leds_per_tile


def unit_converter(unit):
    match units:
        case "inches":
            return unit
        case 'cm':
            return unit / 2.54
        case 'mm':
            return unit / 25.4
        case 'feet':
            return unit * 12
        case 'meters':
            return unit * 39.37


def rectangle_edges(start, end, width):
    # This function remains largely the same as before
    direction = np.array(end) - np.array(start)
    length = np.linalg.norm(direction)
    if length == 0:
        return []  # Prevent division by zero
    direction /= length  # Normalize

    perp_direction = np.array([-direction[1], direction[0]])
    half_width_vector = width / 2 * perp_direction

    v1 = np.array(start) - half_width_vector
    v2 = np.array(start) + half_width_vector
    v3 = np.array(end) + half_width_vector
    v4 = np.array(end) - half_width_vector

    return [v1, v2, v3, v4]  # No need to return to the first vertex for Polygon


def calculate_marker_points(center, radius, angle_degrees, start_offset, line_length):
    angle_rad = np.radians(90 - angle_degrees)
    start_radius = radius * start_offset
    end_radius = start_radius - radius * line_length

    start = (center[0] + start_radius * np.cos(angle_rad),
             center[1] + start_radius * np.sin(angle_rad))
    end = (center[0] + end_radius * np.cos(angle_rad),
           center[1] + end_radius * np.sin(angle_rad))

    return start, end


def calculate_hand_points(center, radius, angle_degrees, hand_length):
    angle_rad = np.radians(90 - angle_degrees)
    end_x = center[0] + radius * hand_length * np.cos(angle_rad)
    end_y = center[1] + radius * hand_length * np.sin(angle_rad)

    return center, (end_x, end_y)


def draw_clock(center, radius, current_hour, current_minute):
    # Draw the clock face
    radius_in_inches = unit_converter(clock_diameter) / 2
    print(f"Drawing clock for {hour}:{minute:02d}")
    if clock_face:
        ax.add_artist(Circle(center, radius_in_inches, edgecolor=clock_face_edge_color, facecolor=clock_face_face_color,
                             lw=clock_face_line_width))

    # Draw lines for every minute
    if add_minute_markers:
        for minute_marker in range(60):
            start, end = calculate_marker_points(center, radius, minute_marker * 6, minute_line_offset,
                                                 minute_line_length)
            ax.plot([start[0], end[0]], [start[1], end[1]], color=minute_line_color, lw=minute_line_width, clip_on=False)

    # Draw line indicators for 12, 3, 6, and 9
    if add_quarter_hour_markers:
        for quarter_marker in [0, 3, 6, 9]:
            start, end = calculate_marker_points(center, radius, quarter_marker * 30, quarter_hour_line_offset,
                                                 quarter_hour_line_length)

            converted_line_width = unit_converter(quarter_hour_line_width)

            # Calculate rectangle corners
            corners = rectangle_edges(start, end, converted_line_width)

            # Draw rectangle as a filled polygon
            if corners:
                polygon = Polygon(corners, closed=True, color=quarter_hour_line_color, edgecolor="none")
                ax.add_patch(polygon)

    # Draw dots for 1, 2, 4, 5, 7, 8, 10, and 11
    if add_5_minute_markers:
        for five_minute_marker in [1, 2, 4, 5, 7, 8, 10, 11]:
            start, end = calculate_marker_points(center, radius, five_minute_marker * 30, five_minute_line_offset,
                                                 five_minute_line_length)

            # Convert line width to millimeters (or to your plotting units)
            converted_line_width = unit_converter(five_minute_line_width)

            # Adjust the end point based on the converted length, if necessary
            # This part is omitted for simplicity as it depends on how you define length

            # Calculate rectangle corners for the polygon
            corners = rectangle_edges(start, end, converted_line_width)

            # Draw rectangle as a filled polygon with specified color
            if corners:
                polygon = Polygon(corners, closed=True, facecolor=five_minute_color,
                                  edgecolor="none")  # Assuming you want no edge line
                ax.add_patch(polygon)

    # Convert hour and minute to angles and radians for the hands
    hour_angle_degrees = (current_hour % 12) * 30 + (current_minute / 60) * 30
    minute_angle_degrees = current_minute * 6

    # Draw hour hand
    hour_hand_start, hour_hand_end = calculate_hand_points(center, radius, hour_angle_degrees, hour_hand_length)

    # Convert hour hand width to your plot's units, if necessary
    converted_hour_hand_width = unit_converter(hour_hand_width)

    # Calculate the corners of the rectangle representing the hour hand
    hour_hand_corners = rectangle_edges(hour_hand_start, hour_hand_end, converted_hour_hand_width)

    # Draw the hour hand as a filled polygon
    if hour_hand_corners:
        hour_hand_polygon = Polygon(hour_hand_corners, closed=True, facecolor=hand_color, edgecolor="none")
        ax.add_patch(hour_hand_polygon)

    # Draw minute hand
    # Calculate the minute hand points
    minute_hand_start, minute_hand_end = calculate_hand_points(center, radius, minute_angle_degrees, minute_hand_length)

    # Convert minute hand width to your plot's units, if necessary
    converted_minute_hand_width = unit_converter(minute_hand_width)

    # Calculate the corners of the rectangle representing the minute hand
    minute_hand_corners = rectangle_edges(minute_hand_start, minute_hand_end, converted_minute_hand_width)

    # Draw the minute hand as a filled polygon
    if minute_hand_corners:
        minute_hand_polygon = Polygon(minute_hand_corners, closed=True, facecolor=hand_color, edgecolor="none")
        ax.add_patch(minute_hand_polygon)


def calculate_position(rows, cols):
    x = (cols + 0.5) * (unit_converter(clock_diameter) + unit_converter(spacing)) + unit_converter(spacing / 2)
    y = fig_height - (
            (rows + 0.5) * (unit_converter(clock_diameter) + unit_converter(spacing)) + unit_converter(spacing / 2))
    return x, y


def get_led_index(n):
    total_width = width_in_tiles * 3
    r = n // total_width
    c = n % total_width
    tile_row = r // 3
    tile_column = c // 3
    within_tile_row = r % 3
    within_tile_column = c % 3
    index_in_tile = within_tile_row * 3 + within_tile_column
    tile_linear_index = tile_row * width_in_tiles + tile_column
    overall_index = tile_linear_index * 9 + index_in_tile
    return overall_index


def generate_lookup_table():
    max_n = width_in_tiles * 3 * height_in_tiles * 3
    lookup_table = [get_led_index(n) for n in range(max_n)]
    return lookup_table


# Prepare the figure
fig_width = (grid_cols * (unit_converter(clock_diameter) + unit_converter(spacing)) + (unit_converter(spacing)))
fig_height = (grid_rows * (unit_converter(clock_diameter) + unit_converter(spacing)) + (unit_converter(spacing)))

fig, ax = plt.subplots(figsize=(fig_width, fig_height))
print(fig_width, fig_height)
ax.set_xlim(0, fig_width)
ax.set_ylim(0, fig_height)
ax.set_aspect('equal')
ax.axis('off')  # Hide the axes
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

times = list(range(720))  # 720 minutes for 12 hours
if randomize_clocks:
    random.shuffle(times)

time_to_position = {}  # Dictionary to hold the time to position mapping

# Draw the clocks and populate the time_to_position dictionary
for i, time in enumerate(times):
    hour = time // 60
    minute = time % 60
    row, col = divmod(i, grid_cols)
    center_x, center_y = calculate_position(row, col)

    # print(f"Drawing clock for {hour}:{minute:02d}")
    draw_clock((center_x, center_y), unit_converter(clock_diameter) / 2, hour, minute)

    # Formatting time for 12-hour clock with AM/PM notation
    formatted_time = f"{hour % 12 if hour % 12 else 12}:{minute:02d}"
    time_to_position[formatted_time] = {"col": col, "row": row}

# Save the figure
plt.savefig("720_clocks.svg", format='svg', facecolor=background_color, edgecolor='none', dpi=100)

# Output the time to position mapping

led_indices = [-1] * 720
for time, pos in time_to_position.items():
    hour, minute = [int(x) for x in time.split(':')]
    minute_index = (hour % 12) * 60 + minute  # Convert time to minute index (0-719)
    led_index = pos['row'] * grid_cols + pos['col']  # Convert row/col to LED index
    led_indices[minute_index] = led_index  # Assign LED index to the correct minute

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

with open("720_clocks_index.txt", "w") as file:
    for time, pos in sorted(time_to_position.items(), key=lambda x: x[1]['row'] * grid_cols + x[1]['col']):
        # Write the formatted string to the file
        file.write(f'"{time}": {{"col": {pos["col"]}, "row": {pos["row"]}}},\n')
