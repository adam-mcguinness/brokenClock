import ezdxf
import numpy as np
import random

# Clock Face and Sizing (unchanged)
clock_face = False
clock_face_edge_color = 'white'
clock_face_face_color = 'none'
clock_face_line_width = 2

# Quarter Hour Markers (unchanged)
add_quarter_hour_markers = True
quarter_hour_line_color = 'black'
quarter_hour_line_length = 0.125
quarter_hour_line_width = .9
quarter_hour_line_offset = 0.95

# 5 Minute Markers (unchanged)
add_5_minute_markers = True
five_minute_color = 'black'
five_minute_line_length = 0.075
five_minute_line_width = 0.5
five_minute_line_offset = 0.95

# 1 Minute Markers (unchanged)
add_minute_markers = False
minute_line_color = 'white'
minute_line_length = 0.05
minute_line_width = 0.25
minute_line_offset = 0.95

# Hands (unchanged)
hand_color = 'black'
hour_hand_length = 0.5
hour_hand_width = 1.25
minute_hand_length = 0.8
minute_hand_width = 1

# Layout and Size (unchanged)
units = 'mm'  # options are inches, cm, mm, feet, and meters
grid_rows, grid_cols = 24, 30
clock_diameter = 30
spacing = 10
background_color = 'white'
randomize_clocks = False

# Tiles for Mapping (unchanged)
leds_per_tile = 3
width_in_tiles = grid_cols // leds_per_tile
height_in_tiles = grid_rows // leds_per_tile

# Function definitions
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

    return [v1.tolist(), v2.tolist(), v3.tolist(), v4.tolist()]

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

# Initialize ezdxf doc
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# Draw functions adapted for ezdxf
def draw_hand_or_marker_with_ezdxf(start, end, width):
    corners = rectangle_edges(start, end, width)
    if corners:
        # Adding the start point at the end to close the polyline
        corners.append(corners[0])
        msp.add_lwpolyline(corners, close=True)

def draw_circle_with_ezdxf(center, radius):
    msp.add_circle(center=center, radius=radius)

def draw_polyline_with_ezdxf(points, close=False):
    # Adding the start point at the end to close the polyline if necessary
    if close:
        points.append(points[0])
    msp.add_lwpolyline(points, close=close)


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('Lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


# The main drawing function
def draw_clock(center, radius, current_hour, current_minute):
    # Minute markers (if enabled)
    if add_minute_markers:
        for minute_marker in range(60):
            start, end = calculate_marker_points(center, radius, minute_marker * 6, minute_line_offset, minute_line_length)
            # Drawing each minute marker as a simple line (a polyline with 2 points)
            draw_polyline_with_ezdxf([start, end])

    # Quarter-hour markers
    if add_quarter_hour_markers:
        for quarter_marker in [0, 3, 6, 9]:
            start, end = calculate_marker_points(center, radius, quarter_marker * 30, quarter_hour_line_offset, quarter_hour_line_length)
            corners = rectangle_edges(start, end, unit_converter(quarter_hour_line_width))
            # Draw the rectangle (for thicker appearance) as a closed polyline
            draw_polyline_with_ezdxf(corners, close=True)

    # 5-minute markers
    if add_5_minute_markers:
        for five_minute_marker in [1, 2, 4, 5, 7, 8, 10, 11]:
            start, end = calculate_marker_points(center, radius, five_minute_marker * 30, five_minute_line_offset, five_minute_line_length)
            corners = rectangle_edges(start, end, unit_converter(five_minute_line_width))
            # Similarly, draw these markers as closed polylines
            draw_polyline_with_ezdxf(corners, close=True)
    # Hour hand
    hour_angle_degrees = (current_hour % 12) * 30 + (current_minute / 60) * 30
    hour_hand_start, hour_hand_end = calculate_hand_points(center, radius, hour_angle_degrees, hour_hand_length)
    converted_hour_hand_width = unit_converter(hour_hand_width)
    draw_hand_or_marker_with_ezdxf(hour_hand_start, hour_hand_end, converted_hour_hand_width)

    # Minute hand
    minute_angle_degrees = current_minute * 6
    minute_hand_start, minute_hand_end = calculate_hand_points(center, radius, minute_angle_degrees, minute_hand_length)
    converted_minute_hand_width = unit_converter(minute_hand_width)
    draw_hand_or_marker_with_ezdxf(minute_hand_start, minute_hand_end, converted_minute_hand_width)

    # Hand attachment circle
    hand_attachment_circle_radius = unit_converter(0.625)  # Example radius, adjust as needed
    draw_circle_with_ezdxf(center, hand_attachment_circle_radius)

    # Add additional elements like markers if needed here
# Calculate position utility (unchanged)
def calculate_position(rows, cols):
    x = (cols + 0.5) * (unit_converter(clock_diameter) + unit_converter(spacing)) + unit_converter(spacing / 2)
    y = (grid_rows - rows - 0.5) * (unit_converter(clock_diameter) + unit_converter(spacing)) + unit_converter(spacing / 2)
    return x, y

# Get LED index (unchanged)
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
# Generate lookup table (unchanged)
def generate_lookup_table():
    max_n = width_in_tiles * 3 * height_in_tiles * 3
    lookup_table = [get_led_index(n) for n in range(max_n)]
    return lookup_table

# Main execution
times = list(range(720))  # 720 minutes for 12 hours
if randomize_clocks:
    random.shuffle(times)

time_to_position = {}  # Dictionary to hold the time to position mapping

for i, time in enumerate(times):
    hour = time // 60
    minute = time % 60
    row, col = divmod(i, grid_cols)
    center_x, center_y = calculate_position(row, col)
    draw_clock((center_x, center_y), unit_converter(clock_diameter) / 2, hour, minute)

# Save the DXF document
doc.saveas("720_clocks.dxf")

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
