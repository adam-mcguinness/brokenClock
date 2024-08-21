import config
from shapely.geometry import Polygon, MultiPolygon


def draw_combined_shape_with_ezdxf(geometry, model_space):
    # Check if the geometry is empty
    if geometry.is_empty:
        return

    # If the geometry is a Polygon, draw it directly
    if isinstance(geometry, Polygon):
        exterior_coords = list(geometry.exterior.coords)
        model_space.add_lwpolyline(exterior_coords, close=True)

    # If the geometry is a MultiPolygon, iterate over each polygon and draw it
    elif isinstance(geometry, MultiPolygon):
        for polygon in geometry.geoms:
            exterior_coords = list(polygon.exterior.coords)
            model_space.add_lwpolyline(exterior_coords, close=True)


def draw_circle_with_ezdxf(center, radius, model_space):
    model_space.add_circle(center=center, radius=radius, close=True)


def draw_polyline_with_ezdxf(points, model_space):
    model_space.add_lwpolyline(points, close=True)


def draw_polyline_boarder(model_space):
    outside_spacing = config.outside_spacing / 2
    center_on_center = config.clock_diameter + config.spacing
    total_width = center_on_center * config.grid_cols + config.spacing
    total_height = center_on_center * config.grid_rows + config.spacing
    # starting as 0,0 we draw a polyline that is offset by the outsize spacing var.
    points = [
        (-outside_spacing, -outside_spacing),
        (-outside_spacing, total_height + outside_spacing),
        (total_width + outside_spacing, total_height + outside_spacing),
        (total_width + outside_spacing, -outside_spacing)
    ]
    model_space.add_lwpolyline(points, close=True)


def calculate_clock_position(rows, cols):
    x = (cols + 0.5) * (config.clock_diameter + config.spacing) + config.spacing / 2
    y = (config.grid_rows - rows - 0.5) * (config.clock_diameter + config.spacing) + config.spacing / 2
    return x, y
