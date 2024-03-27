import config
from unitConverter import unit_converter
import numpy as np
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from drawDxf import draw_polyline_with_ezdxf, draw_combined_shape_with_ezdxf


def draw_clock(clock_style, center, radius, current_hour, current_minute, msp):
    hour_angle_degrees = (current_hour % 12) * 30 + (current_minute / 60) * 30
    hour_hand_start, hour_hand_end = calculate_hand_points(center, radius, hour_angle_degrees,
                                                           config.hour_hand_length)
    minute_angle_degrees = current_minute * 6
    minute_hand_start, minute_hand_end = calculate_hand_points(center, radius, minute_angle_degrees,
                                                               config.minute_hand_length)

    # Minute markers
    if config.add_minute_markers:
        for minute_marker in range(60):
            start, end = calculate_marker_points(center, radius, minute_marker * 6, config.minute_line_offset,
                                                 config.minute_line_length)
            draw_polyline_with_ezdxf([start, end], model_space=msp)

    # 5-minute markers
    if config.add_5_minute_markers:
        for five_minute_marker in [1, 2, 4, 5, 7, 8, 10, 11]:
            start, end = calculate_marker_points(center, radius, five_minute_marker * 30,
                                                 config.five_minute_line_offset,
                                                 config.five_minute_line_length)
            corners = rectangle_edges(start, end, unit_converter(config.five_minute_line_width))
            draw_polyline_with_ezdxf(corners, model_space=msp)

    # Quarter-hour markers
    if config.add_quarter_hour_markers:
        for quarter_marker in [0, 3, 6, 9]:
            start, end = calculate_marker_points(center, radius, quarter_marker * 30,
                                                 config.quarter_hour_line_offset,
                                                 config.quarter_hour_line_length)
            corners = rectangle_edges(start, end, unit_converter(config.quarter_hour_line_width))
            draw_polyline_with_ezdxf(corners, model_space=msp)

    match clock_style:

        case "standard":
            # Create polygons for hour and minute hands
            hour_hand_polygon = create_hand_polygon(hour_hand_start, hour_hand_end,
                                                    unit_converter(config.hour_hand_width))
            minute_hand_polygon = create_hand_polygon(minute_hand_start, minute_hand_end,
                                                      unit_converter(config.minute_hand_width))

            # Create a circle polygon for the hand attachment
            hand_attachment_circle = Point(center).buffer(unit_converter(config.hour_hand_width) / 2 + .005)

            # Combine all shapes
            combined_polygon = unary_union([hour_hand_polygon, minute_hand_polygon, hand_attachment_circle])

            # Draw the combined shape with ezdxf
            draw_combined_shape_with_ezdxf(combined_polygon, model_space=msp)

        case 'notch':
            return

        case 'cutout':
            return


def rectangle_edges(start, end, width):
    direction = np.array(end) - np.array(start)
    length = np.linalg.norm(direction)
    if length == 0:
        return []
    direction /= length

    perp_direction = np.array([-direction[1], direction[0]])
    half_width_vector = width / 2 * perp_direction

    v1 = np.array(start) - half_width_vector
    v2 = np.array(start) + half_width_vector
    v3 = np.array(end) + half_width_vector
    v4 = np.array(end) - half_width_vector

    return [v1.tolist(), v2.tolist(), v3.tolist(), v4.tolist()]


def create_hand_polygon(start, end, width):
    corners = rectangle_edges(start, end, width)
    if corners:
        # Ensure the polygon is closed by repeating the first point
        corners.append(corners[0])
        return Polygon(corners)
    return None


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



