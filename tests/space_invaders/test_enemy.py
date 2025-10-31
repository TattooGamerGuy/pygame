"""Test enemy component with TDD approach."""

import pytest
import pygame
from hub.games.space_invaders.components.enemy import Enemy


class TestEnemyMovement:
    """Test enemy movement and formation."""
    
    def test_enemy_initialization(self, pygame_init):
        """Enemy should initialize with correct values."""
        enemy = Enemy(x=100, y=100, speed=50, enemy_type=1, row=0, col=0)
        
        assert enemy.x == 100
        assert enemy.y == 100
        assert enemy.enemy_type == 1
        assert enemy.row == 0
        assert enemy.col == 0
        assert enemy.initial_x == 100
        assert enemy.initial_y == 100
    
    def test_enemy_moves_right(self, pygame_init):
        """Enemy should move right when direction is 1."""
        enemy = Enemy(x=100, y=100, speed=50, enemy_type=1)
        initial_x = enemy.x
        
        enemy.update(dt=0.1, direction=1)
        
        assert enemy.x > initial_x
    
    def test_enemy_moves_left(self, pygame_init):
        """Enemy should move left when direction is -1."""
        enemy = Enemy(x=100, y=100, speed=50, enemy_type=1)
        initial_x = enemy.x
        
        enemy.update(dt=0.1, direction=-1)
        
        assert enemy.x < initial_x
    
    def test_enemy_formation_tracking(self, pygame_init):
        """Enemy should track formation offset."""
        enemy = Enemy(x=100, y=100, speed=50, enemy_type=1)
        
        # Move enemy
        enemy.update(dt=0.1, direction=1)
        
        # Should track offset
        assert hasattr(enemy, 'formation_offset_x')
        assert enemy.formation_offset_x == enemy.x - enemy.initial_x
    
    def test_enemy_move_down(self, pygame_init):
        """Enemy should move down while maintaining formation."""
        enemy = Enemy(x=100, y=100, speed=50, enemy_type=1)
        initial_y = enemy.y
        initial_initial_y = enemy.initial_y
        
        enemy.move_down(20)
        
        assert enemy.y == initial_y + 20
        assert enemy.initial_y == initial_initial_y + 20
    
    def test_enemy_types(self, pygame_init):
        """Different enemy types should initialize correctly."""
        type1 = Enemy(x=100, y=100, speed=50, enemy_type=1)
        type2 = Enemy(x=100, y=140, speed=50, enemy_type=2)
        type3 = Enemy(x=100, y=180, speed=50, enemy_type=3)
        
        assert type1.enemy_type == 1
        assert type2.enemy_type == 2
        assert type3.enemy_type == 3
    
    def test_enemy_rect(self, pygame_init):
        """Enemy should have correct rectangle."""
        enemy = Enemy(x=100, y=100, speed=50, enemy_type=1)
        rect = enemy.get_rect()
        
        assert rect.x == 100
        assert rect.y == 100
        assert rect.width == 30
        assert rect.height == 20

