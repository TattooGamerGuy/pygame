"""Test bullet component with TDD approach."""

import pytest
import pygame
from hub.games.space_invaders.components.bullet import Bullet
from hub.config.defaults import SCREEN_HEIGHT, SCREEN_WIDTH


class TestBulletDirection:
    """Test bullet direction logic - TDD: tests written first."""
    
    def test_player_bullet_goes_up(self, pygame_init):
        """Player bullets should have negative speed (move UP toward top of screen)."""
        bullet = Bullet(x=400, y=500, speed=400, is_enemy=False)
        
        # Player bullet speed should be negative
        assert bullet.speed < 0, f"Player bullet speed should be negative, got {bullet.speed}"
        assert bullet.speed == -400, f"Expected -400, got {bullet.speed}"
    
    def test_enemy_bullet_goes_down(self, pygame_init):
        """Enemy bullets should have positive speed (move DOWN toward bottom of screen)."""
        bullet = Bullet(x=400, y=100, speed=400, is_enemy=True)
        
        # Enemy bullet speed should be positive
        assert bullet.speed > 0, f"Enemy bullet speed should be positive, got {bullet.speed}"
        assert bullet.speed == 400, f"Expected 400, got {bullet.speed}"
    
    def test_player_bullet_y_decreases(self, pygame_init):
        """Player bullet Y position should decrease when updated (moving up)."""
        bullet = Bullet(x=400, y=500, speed=400, is_enemy=False)
        initial_y = bullet.y
        
        # Update bullet
        bullet.update(dt=0.1)
        
        # Y should decrease (moving toward top where y=0)
        assert bullet.y < initial_y, f"Y should decrease (was {initial_y}, now {bullet.y})"
        assert bullet.y == initial_y - 40, f"Expected Y to decrease by 40 (400 * 0.1), got {bullet.y}"
    
    def test_enemy_bullet_y_increases(self, pygame_init):
        """Enemy bullet Y position should increase when updated (moving down)."""
        bullet = Bullet(x=400, y=100, speed=400, is_enemy=True)
        initial_y = bullet.y
        
        # Update bullet
        bullet.update(dt=0.1)
        
        # Y should increase (moving toward bottom where y=SCREEN_HEIGHT)
        assert bullet.y > initial_y, f"Y should increase (was {initial_y}, now {bullet.y})"
        assert bullet.y == initial_y + 40, f"Expected Y to increase by 40 (400 * 0.1), got {bullet.y}"
    
    def test_bullet_boundaries(self, pygame_init):
        """Bullets should return False when off screen."""
        # Player bullet going up - should disappear at top
        bullet_up = Bullet(x=400, y=0, speed=400, is_enemy=False)
        assert not bullet_up.update(dt=0.1), "Bullet above screen should return False"
        
        # Enemy bullet going down - should disappear at bottom
        bullet_down = Bullet(x=400, y=SCREEN_HEIGHT, speed=400, is_enemy=True)
        assert not bullet_down.update(dt=0.1), "Bullet below screen should return False"
    
    def test_bullet_trail_positions(self, pygame_init):
        """Bullet should track trail positions."""
        bullet = Bullet(x=400, y=500, speed=400, is_enemy=False)
        
        # Update a few times
        for _ in range(3):
            bullet.update(dt=0.1)
        
        # Should have trail positions
        assert len(bullet.trail_positions) > 0, "Bullet should track trail positions"
        assert len(bullet.trail_positions) <= 3, "Trail should not exceed 3 positions"
    
    def test_bullet_rect(self, pygame_init):
        """Bullet should have correct rectangle."""
        bullet = Bullet(x=100, y=200, speed=400, is_enemy=False)
        rect = bullet.get_rect()
        
        assert rect.x == 100
        assert rect.y == 200
        assert rect.width == 4
        assert rect.height == 10

