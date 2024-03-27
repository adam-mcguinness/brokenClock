import ezdxf
import math

from shapely import MultiPolygon
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union

def create_hand_shape(start, end, width):
    """
    Creates a hand shape from the start to the end point with a given width.
    """
    line = LineString([start, end])
    return line.buffer(width / 2, cap_style=2)  # Squared ends

def offset_point_from_center(center, angle, offset):
    """
    Calculates a point offset from the center at a given angle.
    """
    radian_angle = math.radians(angle)
    return (
        center[0] + offset * math.cos(radian_angle),
        center[1] + offset * math.sin(radian_angle)
    )

# Initialize a new DXF document
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# Clock center and radius
clock_center = (0, 0)
clock_radius = 10  # Clock face radius

# Create the main clock face
clock_face = Point(clock_center).buffer(clock_radius)

# Define hand properties
hour_hand_direction = 30  # Example: 30 degrees for the hour hand
minute_hand_direction = 120  # Example: 120 degrees for the minute hand
hour_hand_width = 0.5
minute_hand_width = 0.25
extend_length = 2  # Length by which hands extend beyond the clock radius

# Calculate the starting points for the hour and minute hands one unit inside the clock face
hour_hand_start = offset_point_from_center(clock_center, hour_hand_direction, clock_radius - 1)
minute_hand_start = offset_point_from_center(clock_center, minute_hand_direction, clock_radius - 1)

# Calculate the ending points for the hour and minute hands
hour_hand_end = offset_point_from_center(hour_hand_start, hour_hand_direction, extend_length)
minute_hand_end = offset_point_from_center(minute_hand_start, minute_hand_direction, extend_length)

# Create the hand shapes
hour_hand_shape = create_hand_shape(hour_hand_start, hour_hand_end, hour_hand_width)
minute_hand_shape = create_hand_shape(minute_hand_start, minute_hand_end, minute_hand_width)

# Combine the hour and minute hand shapes
combined_hands_shape = unary_union([hour_hand_shape, minute_hand_shape])

# Subtract the combined hand shape from the clock face to create extended notches
final_clock_face = clock_face.difference(combined_hands_shape)

# Check if the result is a Polygon or a MultiPolygon and handle accordingly
if isinstance(final_clock_face, Polygon):
    final_shape_coords = list(final_clock_face.exterior.coords)
    msp.add_lwpolyline(final_shape_coords)
elif isinstance(final_clock_face, MultiPolygon):
    for polygon in final_clock_face.geoms:
        final_shape_coords = list(polygon.exterior.coords)
        msp.add_lwpolyline(final_shape_coords)

# Save the DXF document
filename = "clock_with_notches_design.dxf"
doc.saveas(filename)
