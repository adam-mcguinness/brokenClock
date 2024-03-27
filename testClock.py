import ezdxf
import math

from shapely import MultiPolygon
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union

def create_extended_hand_shape(center, direction, length, width, extend_length):
    """
    Creates a hand shape extending from the clock center towards a direction with an additional length.
    """
    end_x = center[0] + (length + extend_length) * math.cos(math.radians(direction))
    end_y = center[1] + (length + extend_length) * math.sin(math.radians(direction))
    line = LineString([center, (end_x, end_y)])
    return line.buffer(width / 2, cap_style=3)  # Squared ends

# Initialize a new DXF document
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# Clock center and radius
clock_center = (0, 0)
clock_radius = 10  # Clock face radius

# Define extensions beyond the clock radius for hands
extend_length = 2  # Length by which hands extend beyond the clock radius

# Create the main clock face
clock_face = Point(clock_center).buffer(clock_radius)

# Hour and minute hand directions and lengths
hour_hand_direction = 30  # Example: 30 degrees for the hour hand
minute_hand_direction = 120  # Example: 120 degrees for the minute hand
hour_hand_length = clock_radius  # Use the clock radius as the base length
minute_hand_length = clock_radius  # Similarly for the minute hand

# Create extended hand shapes
hour_hand_shape = create_extended_hand_shape(clock_center, hour_hand_direction, hour_hand_length, 0.5, extend_length)
minute_hand_shape = create_extended_hand_shape(clock_center, minute_hand_direction, minute_hand_length, 0.25, extend_length)

# Combine the hour and minute hand shapes
combined_hands_shape = unary_union([hour_hand_shape, minute_hand_shape])

# Subtract the combined hand shape from the clock face to create extended notches
final_clock_face = clock_face.difference(combined_hands_shape)

# Check if the result is a Polygon or a MultiPolygon and handle accordingly
if isinstance(final_clock_face, Polygon):
    # If the result is a single Polygon, plot it directly
    final_shape_coords = list(final_clock_face.exterior.coords)
    msp.add_lwpolyline(final_shape_coords)
elif isinstance(final_clock_face, MultiPolygon):
    # If the result is a MultiPolygon, iterate over each Polygon using .geoms and plot it
    for polygon in final_clock_face.geoms:
        final_shape_coords = list(polygon.exterior.coords)
        msp.add_lwpolyline(final_shape_coords)

# Draw the modified clock face with extended notches for hands

# Optionally, draw the combined hand shape as a separate object (if desired)
# msp.add_lwpolyline(combined_hands_shape_coords, is_closed=True)

# Save the DXF document
filename = "clock_with_cutouts_design.dxf"
doc.saveas(filename)
