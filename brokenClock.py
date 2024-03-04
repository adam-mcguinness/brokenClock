import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.patches import Circle


def draw_clock(ax, center, radius, hour, minute):
    # Draw the clock face
    clock_face = Circle(center, radius, edgecolor='black', facecolor='white', lw=2)
    ax.add_artist(clock_face)

    # Draw line indicators for 12, 3, 6, and 9
    for i in [0, 3, 6, 9]:
        angle_rad = np.radians(90 - i * 30)  # Convert hours to angle in radians
        inner_offset = 0.8  # Adjust to control how far in the lines start
        line_length = 0.2  # Adjust to control the length of the lines
        start = (center[0] + radius * inner_offset * np.cos(angle_rad),
                 center[1] + radius * inner_offset * np.sin(angle_rad))
        end = (center[0] + (radius * (inner_offset + line_length)) * np.cos(angle_rad),
               center[1] + (radius * (inner_offset + line_length)) * np.sin(angle_rad))
        ax.plot([start[0], end[0]], [start[1], end[1]], color='black', lw=2)

    # Draw dots for 1, 2, 4, 5, 7, 8, 10, and 11
    dot_radius = 0.01  # Size of the dot
    for i in [1, 2, 4, 5, 7, 8, 10, 11]:
        angle_rad = np.radians(90 - i * 30)  # Convert hours to angle in radians
        dot_center = (center[0] + radius * np.cos(angle_rad) * 0.92,  # Adjust position of dot
                      center[1] + radius * np.sin(angle_rad) * 0.92)
        dot = Circle(dot_center, dot_radius, color='black')
        ax.add_artist(dot)

    # Adjust the angle calculations
    # For a clock, 12 o'clock is at 90 degrees, 3 o'clock at 0/360 degrees, 6 o'clock at 270 degrees, and 9 o'clock at 180 degrees
    # Convert hour and minute to angles
    hour_angle = (hour % 12) * 30 + (minute / 60) * 30  # Each hour is 30 degrees, plus a fraction for the minutes
    minute_angle = minute * 6  # Each minute is 6 degrees

    # Convert angles to radians, adjusting for the coordinate system
    # The subtraction from 90 degrees (or π/2 radians) aligns 0 degrees to the top
    hour_angle_rad = np.radians(90 - hour_angle)
    minute_angle_rad = np.radians(90 - minute_angle)

    # Draw hour hand
    hour_length = radius * 0.5
    hour_end = (center[0] + hour_length * np.cos(hour_angle_rad),
                center[1] + hour_length * np.sin(hour_angle_rad))
    ax.plot([center[0], hour_end[0]], [center[1], hour_end[1]], color='black', lw=2)

    # Draw minute hand
    minute_length = radius * 0.8
    minute_end = (center[0] + minute_length * np.cos(minute_angle_rad),
                  center[1] + minute_length * np.sin(minute_angle_rad))
    ax.plot([center[0], minute_end[0]], [center[1], minute_end[1]], color='black', lw=1.5)


def calculate_position(row, col, clock_diameter, spacing, grid_cols, fig_width, fig_height):
    center_x = (col + 0.5) * (clock_diameter + spacing)
    center_y = fig_height - (row + 0.5) * (clock_diameter + spacing)
    return center_x, center_y


# Setup parameters
grid_rows, grid_cols = 24, 30
clock_diameter = 1  # inches
spacing = 0.25  # inches between clocks
fig_width, fig_height = 40, 30  # figure size in inches

# Prepare the figure
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
    center_x, center_y = calculate_position(row, col, clock_diameter, spacing, grid_cols, fig_width, fig_height)

    # Correct radius conversion for drawing
    draw_clock(ax, (center_x, center_y), clock_diameter / 2, hour, minute)

    # Formatting time for 12-hour clock with AM/PM notation
    formatted_time = f"{hour % 12 if hour % 12 else 12}:{minute:02d} {'AM' if hour < 12 else 'PM'}"
    time_to_position[formatted_time] = {"col": col, "row": row}

# Save the figure
plt.savefig("720_clocks.svg", format='svg')

# Output the time to position mapping
filename = "720_clocks_index.txt"
with open(filename, "w") as file:
    for time, pos in sorted(time_to_position.items(), key=lambda x: x[1]['row'] * grid_cols + x[1]['col']):
        # Write the formatted string to the file
        file.write(f'"{time}": {{"col": {pos["col"]}, "row": {pos["row"]}}},\n')
