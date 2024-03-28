import math
import numpy as np
import config
from shapely import LineString
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from drawDxf import draw_combined_shape_with_ezdxf


def draw_clock(clock_style, center, radius, current_hour, current_minute, msp):
    hour_angle_degrees = (current_hour % 12) * 30 + (current_minute / 60) * 30
    minute_angle_degrees = current_minute * 6
    marker_polygons = []
    if config.add_minute_markers:
        for minute_marker in range(60):
            start, end = calculate_marker_points(center, radius, minute_marker * 6, config.minute_line_offset,
                                                 config.minute_line_length)
            corners = rectangle_edges(start, end, config.minute_line_width)
            marker_polygon = Polygon(corners)
            marker_polygons.append(marker_polygon)

    if config.add_5_minute_markers:
        for five_minute_marker in [1, 2, 4, 5, 7, 8, 10, 11]:
            start, end = calculate_marker_points(center, radius, five_minute_marker * 30,
                                                 config.five_minute_line_offset,
                                                 config.five_minute_line_length)
            corners = rectangle_edges(start, end, config.five_minute_line_width)
            marker_polygon = Polygon(corners)
            marker_polygons.append(marker_polygon)

    if config.add_quarter_hour_markers:
        for quarter_marker in [0, 3, 6, 9]:
            start, end = calculate_marker_points(center, radius, quarter_marker * 30,
                                                 config.quarter_hour_line_offset,
                                                 config.quarter_hour_line_length)
            corners = rectangle_edges(start, end, config.quarter_hour_line_width)
            marker_polygon = Polygon(corners)
            marker_polygons.append(marker_polygon)

    match clock_style:

        case "standard":
            hour_hand_start, hour_hand_end = calculate_hand_points(center, radius, hour_angle_degrees,
                                                                   config.hour_hand_length)
            minute_hand_start, minute_hand_end = calculate_hand_points(center, radius, minute_angle_degrees,
                                                                       config.minute_hand_length)

            hour_hand_polygon = create_hand_polygon(hour_hand_start, hour_hand_end,
                                                    config.hour_hand_width)
            minute_hand_polygon = create_hand_polygon(minute_hand_start, minute_hand_end,
                                                      config.minute_hand_width)

            hand_attachment_circle = Point(center).buffer(config.hour_hand_width / 2 + .005)

            all_shapes = [hour_hand_polygon, minute_hand_polygon, hand_attachment_circle] + marker_polygons
            combined_shapes = unary_union(all_shapes)

            draw_combined_shape_with_ezdxf(combined_shapes, model_space=msp)

        case 'notch':
            hour_hand_end = offset_point_from_center(center, hour_angle_degrees - 90, config.clock_diameter / 2)
            hour_hand_start = offset_point_from_center(center, hour_angle_degrees - 90,
                                                       config.clock_diameter / 2 - config.hour_hand_length)

            minute_hand_end = offset_point_from_center(center, minute_angle_degrees - 90, config.clock_diameter / 2)
            minute_hand_start = offset_point_from_center(center, minute_angle_degrees - 90,
                                                         config.clock_diameter / 2 - config.minute_hand_length)

            hour_hand_shape = create_hand_polygon(hour_hand_start, hour_hand_end, config.hour_hand_width)
            minute_hand_shape = create_hand_polygon(minute_hand_start, minute_hand_end, config.minute_hand_width)

            combined_shapes = unary_union([hour_hand_shape, minute_hand_shape] + marker_polygons)

            clock_face = Point(center).buffer(config.clock_diameter / 2)

            final_shape = clock_face.difference(combined_shapes)

            draw_combined_shape_with_ezdxf(final_shape, model_space=msp)

        case 'cutout':
            hour_hand_shape = create_extended_hand_polygon(center, hour_angle_degrees - 90,
                                                           config.hour_hand_length,
                                                           config.hour_hand_width, config.clock_diameter)
            minute_hand_shape = create_extended_hand_polygon(center, minute_angle_degrees - 90,
                                                             config.minute_hand_length,
                                                             config.minute_hand_width, config.clock_diameter)

            all_shapes = [hour_hand_shape, minute_hand_shape] + marker_polygons
            combined_shapes = unary_union(all_shapes)

            clock_face = Point(center).buffer(config.clock_diameter / 2)
            final_clock_face = clock_face.difference(combined_shapes)

            draw_combined_shape_with_ezdxf(final_clock_face, model_space=msp)


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
        corners.append(corners[0])
        return Polygon(corners)
    return None


def create_extended_hand_polygon(center, direction, length, width, extend_length):
    end_x = center[0] + (length + extend_length) * math.cos(math.radians(direction))
    end_y = center[1] - (length + extend_length) * math.sin(math.radians(direction))
    line = LineString([center, (end_x, end_y)])
    return line.buffer(width / 2, cap_style=3)


def calculate_marker_points(center, radius, angle_degrees, start_offset, line_length):
    angle_rad = np.radians(90 - angle_degrees)

    end = (
        center[0] + (radius - start_offset) * np.cos(angle_rad),
        center[1] + (radius - start_offset) * np.sin(angle_rad)
    )

    start = (
        end[0] - line_length * np.cos(angle_rad),
        end[1] - line_length * np.sin(angle_rad)
    )

    return start, end


def calculate_hand_points(center, radius, angle_degrees, hand_length):
    angle_rad = np.radians(90 - angle_degrees)
    end_x = center[0] + hand_length * np.cos(angle_rad)
    end_y = center[1] + hand_length * np.sin(angle_rad)

    return center, (end_x, end_y)


def offset_point_from_center(center, angle, offset):
    radian_angle = math.radians(angle)
    return (
        center[0] + offset * math.cos(radian_angle),
        center[1] - offset * math.sin(radian_angle)
    )