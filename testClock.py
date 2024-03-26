import ezdxf
from math import sin, cos, radians, degrees, atan2

def add_hand_and_arc(msp, center, length, width, angle, arc_radius):
    # Calculate the vector components for the direction of the hand
    angle_rad = radians(angle)
    dx, dy = cos(angle_rad), sin(angle_rad)

    # Calculate the hand's start and end points
    start_x = center[0] + dx * arc_radius
    start_y = center[1] + dy * arc_radius
    end_x = center[0] + dx * (arc_radius + length)
    end_y = center[1] + dy * (arc_radius + length)

    # Determine the perpendicular direction for width
    perp_dx = -dy * width / 2
    perp_dy = dx * width / 2

    # Calculate the endpoints of the hand width
    p1 = (start_x + perp_dx, start_y + perp_dy)
    p2 = (start_x - perp_dx, start_y - perp_dy)
    p3 = (end_x - perp_dx, end_y - perp_dy)
    p4 = (end_x + perp_dx, end_y + perp_dy)

    # Draw the three-sided hand as two lines and a closing line at the end
    msp.add_line(p1, p4)  # Top edge of the hand
    msp.add_line(p4, p3)  # Bottom edge of the hand
    msp.add_line(p3, p2)  # Closing line at the end of the hand

    return p1, p2  # Return the points to connect with the arc

# Initialize a new DXF document
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# Define parameters
center = (100, 100)
hour_hand_length = 60
hour_hand_width = 8
minute_hand_length = 90
minute_hand_width = 6
circle_radius = 15  # The radius for the arcs connecting the hands
hour_angle = 30
minute_angle = 150

# Add hour hand
hour_hand_start, hour_hand_end = add_hand_and_arc(msp, center, hour_hand_length, hour_hand_width, hour_angle, circle_radius)

# Add minute hand
minute_hand_start, minute_hand_end = add_hand_and_arc(msp, center, minute_hand_length, minute_hand_width, minute_angle, circle_radius)

# Draw the arcs to connect the hands to the central circle
# Arc from the end of the hour hand to the start of the minute hand
msp.add_arc(center, circle_radius, start_angle=degrees(atan2(hour_hand_end[1]-center[1], hour_hand_end[0]-center[0])),
            end_angle=degrees(atan2(minute_hand_start[1]-center[1], minute_hand_start[0]-center[0])))

# Arc from the end of the minute hand to the start of the hour hand
msp.add_arc(center, circle_radius, start_angle=degrees(atan2(minute_hand_end[1]-center[1], minute_hand_end[0]-center[0])),
            end_angle=degrees(atan2(hour_hand_start[1]-center[1], hour_hand_start[0]-center[0])))

# Save the DXF file
doc.saveas("clock_design.dxf")
