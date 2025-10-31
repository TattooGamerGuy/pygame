"""Test player component with TDD approach."""

import pytest
import pygame
from hub.games.space_invaders.components.player import Player
from hub.config.defaults import SCREEN_WIDTH


class TestPlayerMovement:
    """Test player movement mechanics."""
    
    def test_player_initialization(self, pygame_init):
        """Player should initialize with correct values."""
        player = Player(x=400, y=500, speed=300)
        
        assert player.x == 400
        assert player.y == 500
        assert player.max_speed == 300
        assert player.velocity == 0.0
    
    def test_player_moves_right(self, pygame_init):
        """Player should move right when direction is 1."""
        player = Player(x=400, y=500, speed=300)
        initial_x = player.x
        
        # Move right
        player.update(dt=0.1, direction=1)
        
        # Should have moved right (x increased)
        assert player.x > initial_x
    
    def test_player_moves_left(self, pygame_init):
        """Player should move left when direction is -1."""
        player = Player(x=400, y=500, speed=300)
        initial_x = player.x
        
        # Move left
        player.update(dt=0.1, direction=-1)
        
        # Should have moved left (x decreased)
        assert player.x < initial_x
    
    def test_player_acceleration(self, pygame_init):
        """Player should accelerate smoothly."""
        player = Player(x=400, y=500, speed=300)
        initial_velocity = player.velocity
        
        # Start moving
        player.update(dt=0.1, direction=1)
        
        # Velocity should have increased
        assert player.velocity > initial_velocity
    
    def test_player_deceleration(self, pygame_init):
        """Player should decelerate when no input."""
        player = Player(x=400, y=500, speed=300)
        
        # Get to max speed first
        for _ in range(5):
            player.update(dt=0.1, direction=1)
        
        max_velocity = player.velocity
        assert max_velocity > 0
        
        # Stop moving
        player.update(dt=0.1, direction=0)
        
        # Velocity should decrease
        assert player.velocity < max_velocity
    
    def test_player_boundary_clamping_left(self, pygame_init):
        """Player should not go off left edge."""
        player = Player(x=0, y=500, speed=300)
        
        # Try to move left
        player.update(dt=1.0, direction=-1)
        
        # Should be clamped to 0
        assert player.x >= 0
    
    def test_player_boundary_clamping_right(self, pygame_init):
        """Player should not go off right edge."""
        player_width = 40  # Player width from component
        player = Player(x=SCREEN_WIDTH - player_width, y=500, speed=300)
        
        # Try to move right
        player.update(dt=1.0, direction=1)
        
        # Should be clamped to screen width
        assert player.x <= SCREEN_WIDTH - player.width
    
    def test_player_rect(self, pygame_init):
        """Player should have correct rectangle."""
        player = Player(x=400, y=500, speed=300)
        rect = player.get_rect()
        
        assert rect.x == 400
        assert rect.y == 500
        assert rect.width == 40
        assert rect.height == 30

