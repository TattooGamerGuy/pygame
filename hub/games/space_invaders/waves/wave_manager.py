"""Wave manager for Space Invaders game progression."""

from typing import List, Optional
from hub.games.space_invaders.waves.wave_config import WaveConfig, get_wave_config
from hub.games.space_invaders.components.enemy import Enemy
from hub.games.space_invaders.constants import (
    ENEMY_ROWS, ENEMY_COLS, ENEMY_SPACING_X, ENEMY_SPACING_Y, ENEMY_START_Y, ENEMY_SPEED
)


class WaveManager:
    """Manages wave progression and enemy formation."""
    
    def __init__(self):
        """Initialize wave manager."""
        self.current_wave = 1
        self.config: Optional[WaveConfig] = None
        self.enemies: List[Enemy] = []
    
    def start_wave(self, wave_number: int) -> List[Enemy]:
        """
        Start a new wave and create enemy formation.
        
        Args:
            wave_number: Wave number to start (1-based)
            
        Returns:
            List of enemy instances
        """
        self.current_wave = wave_number
        self.config = get_wave_config(wave_number)
        self.enemies.clear()
        
        # Create enemy formation based on config
        base_speed = ENEMY_SPEED * self.config.speed_multiplier
        
        for row in range(ENEMY_ROWS):
            enemy_type = self.config.get_enemy_type_for_row(row)
            for col in range(ENEMY_COLS):
                x = col * ENEMY_SPACING_X + 100
                y = row * ENEMY_SPACING_Y + ENEMY_START_Y
                enemy = Enemy(x, y, base_speed, enemy_type=enemy_type, row=row, col=col)
                self.enemies.append(enemy)
        
        return self.enemies
    
    def get_enemies(self) -> List[Enemy]:
        """Get current wave enemies."""
        return self.enemies
    
    def remove_enemy(self, enemy: Enemy) -> None:
        """Remove enemy from wave."""
        if enemy in self.enemies:
            self.enemies.remove(enemy)
    
    def is_wave_complete(self) -> bool:
        """Check if current wave is complete (all enemies destroyed)."""
        return len(self.enemies) == 0
    
    def get_move_interval(self) -> float:
        """Get enemy move interval for current wave."""
        return self.config.move_interval if self.config else 1.0
    
    def get_shoot_interval(self) -> float:
        """Get enemy shoot interval for current wave."""
        return self.config.shoot_interval if self.config else 1.5
    
    def get_ufo_spawn_chance(self) -> float:
        """Get UFO spawn chance per second for current wave."""
        return self.config.ufo_spawn_chance if self.config else 0.3
    
    def get_current_wave(self) -> int:
        """Get current wave number."""
        return self.current_wave

