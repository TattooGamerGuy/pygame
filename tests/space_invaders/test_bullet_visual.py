"""Test bullet visual rendering (TDD for visual bug fix)."""

import pytest
import pygame
from hub.games.space_invaders.components.bullet import Bullet
from hub.config.defaults import SCREEN_HEIGHT


class TestBulletVisualRendering:
    """Test that bullets render in correct position visually."""
    
    def test_player_bullet_spawn_position(self, pygame_init):
        """Player bullet should spawn at top of ship, not bottom."""
        from hub.config.defaults import SCREEN_HEIGHT
        
        # Player is at bottom of screen
        player_y = SCREEN_HEIGHT - 60
        player_height = 30
        
        # Bullet spawns at player.y (top of ship)
        bullet = Bullet(400, player_y, 400, is_enemy=False)
        
        # Bullet should be at top of player ship
        assert bullet.y == player_y, f"Bullet should spawn at top of player ({player_y}), got {bullet.y}"
        
        # Bullet rect top should be near player top
        rect = bullet.get_rect()
        assert abs(rect.y - player_y) < 5, "Bullet should render near player top"
    
    def test_player_bullet_moves_up_from_spawn(self, pygame_init):
        """Player bullet Y should decrease immediately after spawn (going up)."""
        player_y = SCREEN_HEIGHT - 60
        bullet = Bullet(400, player_y, 400, is_enemy=False)
        
        initial_y = bullet.y
        bullet.update(0.016)  # 1 frame at 60fps
        
        assert bullet.y < initial_y, \
            f"Bullet Y should decrease (was {initial_y}, now {bullet.y}) - going UP toward enemies"
        assert bullet.speed < 0, f"Bullet speed should be negative ({bullet.speed})"
    
    def test_bullet_rendering_position_after_update(self, pygame_init, mock_surface):
        """Bullet should render at correct visual position after moving."""
        player_y = SCREEN_HEIGHT - 60
        bullet = Bullet(400, player_y, 400, is_enemy=False)
        
        # Update bullet (moves up)
        bullet.update(0.1)
        
        # Render bullet
        bullet.render(mock_surface)
        rect = bullet.get_rect()
        
        # After moving up, Y should be less than initial spawn
        assert rect.y < player_y, \
            f"After moving up, bullet Y ({rect.y}) should be less than spawn Y ({player_y})"
    
    def test_bullet_direction_consistency(self, pygame_init):
        """Bullet direction should be consistent: negative speed = Y decreases."""
        bullet = Bullet(400, 500, 400, is_enemy=False)
        
        # Negative speed means going UP (Y decreases)
        assert bullet.speed < 0
        
        y1 = bullet.y
        bullet.update(0.1)
        y2 = bullet.y
        
        assert y2 < y1, f"Negative speed should decrease Y (was {y1}, now {y2})"

