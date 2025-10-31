"""Test shield component with TDD approach."""

import pytest
import pygame
from hub.games.space_invaders.components.shield import Shield
from hub.games.space_invaders.components.bullet import Bullet


class TestShieldMechanics:
    """Test shield barrier mechanics."""
    
    def test_shield_initialization(self, pygame_init):
        """Shield should initialize with correct dimensions."""
        shield = Shield(x=100, y=500, width=80, height=60)
        
        assert shield.x == 100
        assert shield.y == 500
        assert shield.width == 80
        assert shield.height == 60
        assert len(shield.damage_mask) > 0
    
    def test_shield_shape_initialization(self, pygame_init):
        """Shield should have proper shape (arc at top)."""
        shield = Shield(x=100, y=500, width=80, height=60)
        
        # Top rows should have some destroyed segments (arc opening)
        top_row_has_gaps = any(shield.damage_mask[0])
        assert top_row_has_gaps, "Top row should have arc opening"
    
    def test_bullet_hits_shield(self, pygame_init):
        """Bullet should collide with shield."""
        shield = Shield(x=100, y=500, width=80, height=60)
        bullet = Bullet(x=130, y=510, speed=400, is_enemy=False)
        
        bullet_rect = bullet.get_rect()
        hit = shield.check_bullet_collision(bullet_rect)
        
        assert hit, "Bullet should hit shield"
    
    def test_bullet_misses_shield(self, pygame_init):
        """Bullet far from shield should not collide."""
        shield = Shield(x=100, y=500, width=80, height=60)
        bullet = Bullet(x=500, y=510, speed=400, is_enemy=False)
        
        bullet_rect = bullet.get_rect()
        hit = shield.check_bullet_collision(bullet_rect)
        
        assert not hit, "Distant bullet should not hit shield"
    
    def test_shield_damage_progresses(self, pygame_init):
        """Shield should accumulate damage from multiple hits."""
        shield = Shield(x=100, y=500, width=80, height=60)
        initial_damaged = sum(sum(row) for row in shield.damage_mask)
        
        # Hit shield multiple times
        for i in range(5):
            bullet = Bullet(x=130 + i*5, y=510, speed=400, is_enemy=False)
            shield.check_bullet_collision(bullet.get_rect())
        
        final_damaged = sum(sum(row) for row in shield.damage_mask)
        assert final_damaged > initial_damaged, "Shield should accumulate damage"
    
    def test_shield_not_destroyed_initially(self, pygame_init):
        """Shield should not be completely destroyed initially."""
        shield = Shield(x=100, y=500, width=80, height=60)
        
        assert not shield.is_destroyed(), "Shield should not be destroyed initially"
    
    def test_shield_rect(self, pygame_init):
        """Shield should have correct bounding rectangle."""
        shield = Shield(x=100, y=500, width=80, height=60)
        rect = shield.get_rect()
        
        assert rect.x == 100
        assert rect.y == 500
        assert rect.width == 80
        assert rect.height == 60

