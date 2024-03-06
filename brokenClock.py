import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.patches import Circle

# Clock Face and Sizing
clock_face = True
clock_face_edge_color = 'white'
clock_face_face_color = 'none'
clock_face_line_width = 2

# Quarter Hour Markers
add_quarter_hour_markers = False
quarter_hour_line_color = 'white'
quarter_hour_line_length = 0.1
quarter_hour_line_width = 1
quarter_hour_line_offset = 0.95

# 5 Minute Markers
add_5_minute_markers = False
five_minute_color = 'white'
five_minute_line_length = 0.1
five_minute_line_width = 1
five_minute_line_offset = 0.95

# 1 Minute Markers
add_minute_markers = False
minute_line_color = 'white'
minute_line_length = 0.05
minute_line_width = 0.25
minute_line_offset = 0.95

# Hands
hand_color = 'white'
hour_hand_length = 0.5
hour_hand_width = 2
minute_hand_length = 0.8
minute_hand_width = 1.5

# Layout and Size
grid_rows, grid_cols = 24, 30
clock_diameter = 1.5  # inches
spacing = 0.5  # inches between clocks
background_color = 'black'


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
    if clock_face:
        ax.add_artist(Circle(center, radius, edgecolor=clock_face_edge_color, facecolor=clock_face_face_color,
                             lw=clock_face_line_width))

    # Draw lines for every minute
    if add_minute_markers:
        for minute_marker in range(60):
            start, end = calculate_marker_points(center, radius, minute_marker * 6, minute_line_offset,
                                                 minute_line_length)
            ax.plot([start[0], end[0]], [start[1], end[1]], color=minute_line_color, lw=minute_line_width)

    # Draw line indicators for 12, 3, 6, and 9
    if add_quarter_hour_markers:
        for quarter_maker in [0, 3, 6, 9]:
            start, end = calculate_marker_points(center, radius, quarter_maker * 30, quarter_hour_line_offset,
                                                 quarter_hour_line_length)
            ax.plot([start[0], end[0]], [start[1], end[1]], color=quarter_hour_line_color, lw=quarter_hour_line_width)

    # Draw dots for 1, 2, 4, 5, 7, 8, 10, and 11
    if add_5_minute_markers:
        for five_minute_marker in [1, 2, 4, 5, 7, 8, 10, 11]:
            start, end = calculate_marker_points(center, radius, five_minute_marker * 30, five_minute_line_offset,
                                                 five_minute_line_length)
            ax.plot([start[0], end[0]], [start[1], end[1]], color=five_minute_color, lw=five_minute_line_width)

    # Convert hour and minute to angles and radians for the hands
    hour_angle_degrees = (current_hour % 12) * 30 + (current_minute / 60) * 30
    minute_angle_degrees = current_minute * 6

    # Draw hour hand
    hour_hand_start, hour_hand_end = calculate_hand_points(center, radius, hour_angle_degrees, hour_hand_length)
    ax.plot([hour_hand_start[0], hour_hand_end[0]], [hour_hand_start[1], hour_hand_end[1]], color=hand_color,
            lw=hour_hand_width)

    # Draw minute hand
    minute_hand_start, minute_hand_end = calculate_hand_points(center, radius, minute_angle_degrees, minute_hand_length)
    ax.plot([minute_hand_start[0], minute_hand_end[0]], [minute_hand_start[1], minute_hand_end[1]], color=hand_color,
            lw=minute_hand_width)


def calculate_position(rows, cols):
    x = (cols + 0.5) * (clock_diameter + spacing)
    y = fig_height - (rows + 0.5) * (clock_diameter + spacing)
    return x, y


# Prepare the figure
fig_width, fig_height = (grid_cols * clock_diameter) + (grid_cols * spacing), (grid_rows * clock_diameter) + (
        grid_rows * spacing)
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.set_xlim(0, fig_width)
ax.set_ylim(0, fig_height)
ax.axis('off')  # Hide the axes

times = list(range(720))  # 720 minutes for 12 hours
random.shuffle(times)

time_to_position = {}  # Dictionary to hold the time to position mapping

# Draw the clocks and populate the time_to_position dictionary
for i, time in enumerate(times):
    hour = time // 60
    minute = time % 60
    row, col = divmod(i, grid_cols)
    center_x, center_y = calculate_position(row, col)

    # Correct radius conversion for drawing
    print(f"Drawing clock for {hour}:{minute:02d}")
    draw_clock((center_x, center_y), clock_diameter / 2, hour, minute)

    # Formatting time for 12-hour clock with AM/PM notation
    formatted_time = f"{hour % 12 if hour % 12 else 12}:{minute:02d}"
    time_to_position[formatted_time] = {"col": col, "row": row}

# Save the figure
plt.savefig("720_clocks.svg", format='svg', bbox_inches='tight', facecolor=background_color, edgecolor='none')

# Output the time to position mapping

with open("720_clocks_index.txt", "w") as file:
    for time, pos in sorted(time_to_position.items(), key=lambda x: x[1]['row'] * grid_cols + x[1]['col']):
        # Write the formatted string to the file
        file.write(f'"{time}": {{"col": {pos["col"]}, "row": {pos["row"]}}},\n')
