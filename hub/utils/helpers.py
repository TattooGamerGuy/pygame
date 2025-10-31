"""General utility functions."""

from typing import Tuple, Optional
import math


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def lerp(a: float, b: float, t: float) -> float:
    """
    Linear interpolation between a and b.
    
    Args:
        a: Start value
        b: End value
        t: Interpolation factor (0.0 to 1.0)
        
    Returns:
        Interpolated value
    """
    return a + (b - a) * clamp(t, 0.0, 1.0)


def distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """
    Calculate distance between two points.
    
    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)
        
    Returns:
        Distance
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.sqrt(dx * dx + dy * dy)


def normalize_angle(angle: float) -> float:
    """
    Normalize angle to 0-360 range.
    
    Args:
        angle: Angle in degrees
        
    Returns:
        Normalized angle
    """
    while angle < 0:
        angle += 360
    while angle >= 360:
        angle -= 360
    return angle


def point_in_rect(point: Tuple[float, float], rect: Tuple[float, float, float, float]) -> bool:
    """
    Check if point is inside rectangle.
    
    Args:
        point: Point (x, y)
        rect: Rectangle (x, y, width, height)
        
    Returns:
        True if point is inside
    """
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


def center_text(text_width: int, text_height: int, container_width: int, container_height: int) -> Tuple[int, int]:
    """
    Calculate position to center text in container.
    
    Args:
        text_width: Text width
        text_height: Text height
        container_width: Container width
        container_height: Container height
        
    Returns:
        Position (x, y) to center text
    """
    x = (container_width - text_width) // 2
    y = (container_height - text_height) // 2
    return (x, y)

