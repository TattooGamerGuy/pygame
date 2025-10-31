"""Programmatic 8-bit sprite drawing functions for Space Invaders."""

from typing import Tuple, Optional
import pygame
from hub.config.defaults import GREEN, WHITE, YELLOW, CYAN, RED, BLACK


def draw_player_ship(surface: pygame.Surface, x: float, y: float, width: int = 40, height: int = 30) -> None:
    """
    Draw classic Space Invaders player ship sprite.
    
    Args:
        surface: Surface to draw on
        x: Center X position
        y: Center Y position
        width: Ship width
        height: Ship height
    """
    center_x = int(x)
    center_y = int(y)
    
    # Main body (rectangular base)
    body_rect = pygame.Rect(center_x - width // 2 + 2, center_y - height // 2 + 10, width - 4, height - 10)
    pygame.draw.rect(surface, GREEN, body_rect)
    
    # Top cannon/shield (triangle shape)
    points = [
        (center_x, center_y - height // 2),
        (center_x - width // 3, center_y - height // 2 + 8),
        (center_x + width // 3, center_y - height // 2 + 8),
    ]
    pygame.draw.polygon(surface, GREEN, points)
    
    # Side wings
    wing_width = width // 4
    wing_height = height // 3
    # Left wing
    pygame.draw.rect(surface, GREEN, 
                    (center_x - width // 2, center_y - height // 2 + 5, wing_width, wing_height))
    # Right wing
    pygame.draw.rect(surface, GREEN, 
                    (center_x + width // 2 - wing_width, center_y - height // 2 + 5, wing_width, wing_height))


def draw_enemy_type1(surface: pygame.Surface, x: float, y: float, width: int = 30, height: int = 20, frame: int = 0) -> None:
    """
    Draw top row enemy (Type 1) - crab-like, 30 points.
    
    Args:
        surface: Surface to draw on
        x: Center X position
        y: Center Y position
        width: Enemy width
        height: Enemy height
        frame: Animation frame (0 or 1 for crab leg animation)
    """
    center_x = int(x)
    center_y = int(y)
    
    # Main body (oval-ish rectangle)
    body_rect = pygame.Rect(center_x - width // 2 + 3, center_y - height // 2 + 2, width - 6, height - 4)
    pygame.draw.ellipse(surface, YELLOW, body_rect)
    
    # Top eyes
    eye_size = 3
    pygame.draw.circle(surface, BLACK, (center_x - 6, center_y - 4), eye_size)
    pygame.draw.circle(surface, BLACK, (center_x + 6, center_y - 4), eye_size)
    
    # Claws/pincers (animate with frame)
    offset = 2 if frame == 0 else -2
    # Left pincer
    pincer_points_left = [
        (center_x - width // 2, center_y),
        (center_x - width // 2 - 4 + offset, center_y - 3),
        (center_x - width // 2 - 2 + offset, center_y),
    ]
    pygame.draw.polygon(surface, YELLOW, pincer_points_left)
    
    # Right pincer
    pincer_points_right = [
        (center_x + width // 2, center_y),
        (center_x + width // 2 + 4 - offset, center_y - 3),
        (center_x + width // 2 + 2 - offset, center_y),
    ]
    pygame.draw.polygon(surface, YELLOW, pincer_points_right)
    
    # Legs (bottom)
    leg_width = 3
    for i in range(3):
        leg_offset = (i - 1) * 8
        pygame.draw.rect(surface, YELLOW, 
                        (center_x + leg_offset - 1, center_y + height // 2 - 2, leg_width, 4))


def draw_enemy_type2(surface: pygame.Surface, x: float, y: float, width: int = 30, height: int = 20, frame: int = 0) -> None:
    """
    Draw middle row enemy (Type 2) - squid-like, 20 points.
    
    Args:
        surface: Surface to draw on
        x: Center X position
        y: Center Y position
        width: Enemy width
        height: Enemy height
        frame: Animation frame (0 or 1 for tentacle animation)
    """
    center_x = int(x)
    center_y = int(y)
    
    # Main body (more rounded)
    body_rect = pygame.Rect(center_x - width // 2 + 2, center_y - height // 2, width - 4, height)
    pygame.draw.ellipse(surface, CYAN, body_rect)
    
    # Top dome/head
    pygame.draw.ellipse(surface, CYAN, 
                       (center_x - width // 3, center_y - height // 2 - 3, width * 2 // 3, height // 2))
    
    # Eyes
    pygame.draw.circle(surface, BLACK, (center_x - 5, center_y - 2), 2)
    pygame.draw.circle(surface, BLACK, (center_x + 5, center_y - 2), 2)
    
    # Tentacles (animate with frame)
    tentacle_offset = 1 if frame == 0 else -1
    for i in range(4):
        tent_x = center_x - width // 2 + 6 + i * 5
        tent_y = center_y + height // 2
        # Tentacle curves
        points = [
            (tent_x, tent_y),
            (tent_x + tentacle_offset, tent_y + 4),
            (tent_x - tentacle_offset, tent_y + 6),
        ]
        for j in range(len(points) - 1):
            pygame.draw.line(surface, CYAN, points[j], points[j + 1], 2)


def draw_enemy_type3(surface: pygame.Surface, x: float, y: float, width: int = 30, height: int = 20, frame: int = 0) -> None:
    """
    Draw bottom row enemy (Type 3) - octopus-like, 10 points.
    
    Args:
        surface: Surface to draw on
        x: Center X position
        y: Center Y position
        width: Enemy width
        height: Enemy height
        frame: Animation frame (0 or 1 for leg animation)
    """
    center_x = int(x)
    center_y = int(y)
    
    # Main body (larger, flatter)
    body_rect = pygame.Rect(center_x - width // 2, center_y - height // 2 + 2, width, height - 4)
    pygame.draw.rect(surface, RED, body_rect)
    
    # Top detail
    pygame.draw.rect(surface, RED, 
                    (center_x - width // 3, center_y - height // 2, width * 2 // 3, height // 3))
    
    # Eyes
    pygame.draw.circle(surface, BLACK, (center_x - 6, center_y), 3)
    pygame.draw.circle(surface, BLACK, (center_x + 6, center_y), 3)
    
    # Legs/arms (animate with frame)
    leg_offset = 2 if frame == 0 else -2
    for i in range(4):
        leg_x = center_x - width // 2 + 4 + i * 6
        leg_y = center_y + height // 2 - 2
        
        # Left side leg
        if i < 2:
            pygame.draw.line(surface, RED, (leg_x, leg_y), 
                           (leg_x - 3 + leg_offset, leg_y + 4), 2)
        # Right side leg
        else:
            pygame.draw.line(surface, RED, (leg_x, leg_y), 
                           (leg_x + 3 - leg_offset, leg_y + 4), 2)


def draw_ufo(surface: pygame.Surface, x: float, y: float, width: int = 48, height: int = 16) -> None:
    """
    Draw UFO bonus enemy sprite.
    
    Args:
        surface: Surface to draw on
        x: Center X position
        y: Center Y position
        width: UFO width
        height: UFO height
    """
    center_x = int(x)
    center_y = int(y)
    
    # Main body (elongated ellipse)
    body_rect = pygame.Rect(center_x - width // 2, center_y - height // 2, width, height)
    pygame.draw.ellipse(surface, GREEN, body_rect)
    
    # Top dome
    dome_rect = pygame.Rect(center_x - width // 3, center_y - height // 2 - 4, width * 2 // 3, height // 2)
    pygame.draw.ellipse(surface, YELLOW, dome_rect)
    
    # Windows/details
    for i in range(3):
        window_x = center_x - width // 4 + i * (width // 4)
        pygame.draw.circle(surface, CYAN, (window_x, center_y), 3)
    
    # Bottom fins
    fin_height = 4
    pygame.draw.polygon(surface, GREEN, [
        (center_x - width // 2 + 4, center_y + height // 2),
        (center_x - width // 4, center_y + height // 2 + fin_height),
        (center_x - width // 2 + 8, center_y + height // 2),
    ])
    pygame.draw.polygon(surface, GREEN, [
        (center_x + width // 2 - 4, center_y + height // 2),
        (center_x + width // 4, center_y + height // 2 + fin_height),
        (center_x + width // 2 - 8, center_y + height // 2),
    ])


def draw_shield(surface: pygame.Surface, x: float, y: float, width: int = 80, height: int = 60) -> None:
    """
    Draw shield barrier sprite.
    
    Args:
        surface: Surface to draw on
        x: Center X position
        y: Center Y position
        width: Shield width
        height: Shield height
    """
    center_x = int(x)
    center_y = int(y)
    
    # Main shield arc (top curve)
    # Draw using multiple small rectangles to create curve
    arc_height = height // 3
    
    # Top arc
    for i in range(arc_height):
        curve_width = int(width * (1 - (i / arc_height) ** 2) ** 0.5)
        if curve_width > 0:
            rect_x = center_x - curve_width // 2
            rect_y = center_y - height // 2 + i
            pygame.draw.rect(surface, GREEN, (rect_x, rect_y, curve_width, 1))
    
    # Left wall
    pygame.draw.rect(surface, GREEN, 
                    (center_x - width // 2, center_y - height // 2 + arc_height, 
                     width // 6, height - arc_height))
    
    # Right wall
    pygame.draw.rect(surface, GREEN, 
                    (center_x + width // 2 - width // 6, center_y - height // 2 + arc_height, 
                     width // 6, height - arc_height))
    
    # Bottom base
    pygame.draw.rect(surface, GREEN, 
                    (center_x - width // 2 + width // 6, center_y + height // 2 - height // 4, 
                     width - width // 3, height // 4))


def draw_shield_damage(surface: pygame.Surface, x: float, y: float, damage_mask: list, segment_size: int = 4) -> None:
    """
    Draw damaged shield segments based on damage mask.
    
    Args:
        surface: Surface to draw on
        x: Shield top-left X position
        y: Shield top-left Y position
        damage_mask: 2D list of booleans (True = damaged/destroyed)
        segment_size: Size of each segment in pixels
    """
    for row_idx, row in enumerate(damage_mask):
        for col_idx, is_damaged in enumerate(row):
            if is_damaged:
                # Draw black/destroyed segment
                seg_x = int(x) + col_idx * segment_size
                seg_y = int(y) + row_idx * segment_size
                pygame.draw.rect(surface, BLACK, 
                               (seg_x, seg_y, segment_size, segment_size))


def draw_explosion(surface: pygame.Surface, x: float, y: float, frame: int, size: int = 20) -> None:
    """
    Draw explosion animation.
    
    Args:
        surface: Surface to draw on
        x: Center X position
        y: Center Y position
        frame: Animation frame (0-3)
        size: Base explosion size
    """
    center_x = int(x)
    center_y = int(y)
    
    # Explosion grows then shrinks
    if frame < 2:
        explosion_size = size + frame * 4
        color_intensity = 255 - frame * 60
    else:
        explosion_size = size + (4 - frame) * 2
        color_intensity = 180 - (frame - 2) * 60
    
    color = (min(255, color_intensity), min(255, color_intensity // 2), 0)
    
    # Draw explosion as expanding circles
    for i in range(3):
        radius = explosion_size // 3 * (i + 1)
        alpha = 200 - i * 60
        if radius > 0:
            # Create temporary surface for transparency
            temp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (*color, alpha), (radius, radius), radius)
            surface.blit(temp_surf, (center_x - radius, center_y - radius))

