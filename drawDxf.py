import config


def draw_combined_shape_with_ezdxf(polygon, model_space):
    if polygon.is_empty:
        return
    exterior_coords = list(polygon.exterior.coords)
    model_space.add_lwpolyline(exterior_coords, close=True)


def draw_circle_with_ezdxf(center, radius, model_space):
    model_space.add_circle(center=center, radius=radius, close=True)


def draw_polyline_with_ezdxf(points, model_space):
    model_space.add_lwpolyline(points, close=True)


def calculate_clock_position(rows, cols):
    x = (cols + 0.5) * (config.clock_diameter + config.spacing) + config.spacing / 2
    y = (config.grid_rows - rows - 0.5) * (config.clock_diameter + config.spacing) + config.spacing / 2
    return x, y
