"""Wave configuration for Space Invaders."""

from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class WaveConfig:
    """Configuration for a wave."""
    wave_number: int
    enemy_rows: int = 5
    enemy_cols: int = 10
    enemy_spacing_x: int = 50
    enemy_spacing_y: int = 40
    start_y: int = 100
    speed_multiplier: float = 1.0
    move_interval: float = 1.0
    shoot_interval: float = 1.5
    ufo_spawn_chance: float = 0.3  # Chance per second
    
    def get_enemy_type_for_row(self, row: int) -> int:
        """
        Get enemy type based on row position.
        
        Args:
            row: Row index (0-based from top)
            
        Returns:
            Enemy type (1, 2, or 3)
        """
        if row == 0:
            return 1  # Top row - Type 1 (30 points)
        elif row < 3:
            return 2  # Middle rows - Type 2 (20 points)
        else:
            return 3  # Bottom rows - Type 3 (10 points)


def get_wave_config(wave_number: int) -> WaveConfig:
    """
    Get configuration for a specific wave with progressive difficulty.
    
    Args:
        wave_number: Wave number (1-based)
        
    Returns:
        Wave configuration
    """
    base_config = WaveConfig(wave_number=wave_number)
    
    # Progressive difficulty scaling
    # Speed increases steadily but caps at 2.5x
    speed_multiplier = min(2.5, 1.0 + (wave_number - 1) * 0.12)
    
    # Move interval decreases (enemies move faster) but doesn't go below 0.25s
    move_interval = max(0.25, 1.0 - (wave_number - 1) * 0.06)
    
    # Shooting interval decreases (more frequent shooting) but caps at 0.7s
    shoot_interval = max(0.7, 1.5 - (wave_number - 1) * 0.06)
    
    # UFO spawn chance increases but caps at 0.6
    ufo_spawn_chance = min(0.6, 0.3 + (wave_number - 1) * 0.025)
    
    # Special wave mechanics (every 5 waves gets slightly harder)
    wave_tier = (wave_number - 1) // 5
    if wave_tier > 0:
        speed_multiplier *= (1.0 + wave_tier * 0.1)
        move_interval *= (1.0 - wave_tier * 0.05)
        shoot_interval *= (1.0 - wave_tier * 0.05)
    
    return WaveConfig(
        wave_number=wave_number,
        speed_multiplier=speed_multiplier,
        move_interval=max(0.2, move_interval),  # Final safety cap
        shoot_interval=max(0.6, shoot_interval),  # Final safety cap
        ufo_spawn_chance=min(0.65, ufo_spawn_chance)
    )

