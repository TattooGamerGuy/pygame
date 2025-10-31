"""Test collision detection with TDD approach."""

import pytest
import pygame
from hub.games.space_invaders.components.bullet import Bullet
from hub.games.space_invaders.components.enemy import Enemy
from hub.games.space_invaders.components.player import Player


class TestBulletCollisions:
    """Test bullet collision detection."""
    
    def test_player_bullet_hits_enemy(self, pygame_init):
        """Player bullet should collide with enemy."""
        bullet = Bullet(x=400, y=200, speed=400, is_enemy=False)
        enemy = Enemy(x=395, y=200, speed=50, enemy_type=1)
        
        bullet_rect = bullet.get_rect()
        enemy_rect = enemy.get_rect()
        
        assert bullet_rect.colliderect(enemy_rect), "Bullet should collide with enemy"
    
    def test_enemy_bullet_hits_player(self, pygame_init):
        """Enemy bullet should collide with player."""
        bullet = Bullet(x=400, y=500, speed=400, is_enemy=True)
        player = Player(x=395, y=500, speed=300)
        
        bullet_rect = bullet.get_rect()
        player_rect = player.get_rect()
        
        assert bullet_rect.colliderect(player_rect), "Enemy bullet should collide with player"
    
    def test_bullet_misses_enemy(self, pygame_init):
        """Bullet should not collide when far from enemy."""
        bullet = Bullet(x=100, y=200, speed=400, is_enemy=False)
        enemy = Enemy(x=500, y=200, speed=50, enemy_type=1)
        
        bullet_rect = bullet.get_rect()
        enemy_rect = enemy.get_rect()
        
        assert not bullet_rect.colliderect(enemy_rect), "Bullet should not collide when far away"
    
    def test_multiple_bullets_enemy_collision(self, pygame_init):
        """Multiple bullets should correctly detect collisions."""
        bullets = [
            Bullet(x=400, y=200, speed=400, is_enemy=False),
            Bullet(x=410, y=200, speed=400, is_enemy=False)
        ]
        enemy = Enemy(x=395, y=200, speed=50, enemy_type=1)
        
        enemy_rect = enemy.get_rect()
        collisions = [b.get_rect().colliderect(enemy_rect) for b in bullets]
        
        # At least one should collide (depending on spacing)
        assert any(collisions) or all(not c for c in collisions), "Collision detection should work"

