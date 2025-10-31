"""Integration tests for Space Invaders game (TDD approach)."""

import pytest
import pygame
from unittest.mock import Mock, MagicMock
from hub.games.space_invaders.game.game import SpaceInvadersGameModular
from hub.core.display import DisplayManager
from hub.services.input_service import InputService
from hub.services.audio_service import AudioService
from hub.events.event_bus import EventBus


class TestGameIntegration:
    """Integration tests for full game mechanics."""
    
    @pytest.fixture
    def mock_services(self, pygame_init):
        """Create mock services for game."""
        display = MagicMock(spec=DisplayManager)
        # Set up display - it's a property, not a method
        screen_surface = pygame.Surface((800, 600))
        type(display).screen = screen_surface
        type(display).width = 800
        type(display).height = 600
        type(display).size = (800, 600)
        
        input_service = MagicMock(spec=InputService)
        input_service.is_key_pressed = Mock(return_value=False)
        input_service.is_key_just_pressed = Mock(return_value=False)
        
        audio_service = MagicMock(spec=AudioService)
        event_bus = MagicMock(spec=EventBus)
        
        return {
            'display': display,
            'input': input_service,
            'audio': audio_service,
            'event_bus': event_bus
        }
    
    def test_game_initialization(self, mock_services):
        """Game should initialize correctly."""
        game = SpaceInvadersGameModular(
            mock_services['display'],
            mock_services['input'],
            mock_services['audio'],
            mock_services['event_bus']
        )
        
        assert game is not None
        assert game.current_wave == 1
        assert game.lives > 0
    
    def test_player_shooting_creates_bullet(self, mock_services, pygame_init):
        """Player shooting should create bullet going UP."""
        game = SpaceInvadersGameModular(
            mock_services['display'],
            mock_services['input'],
            mock_services['audio'],
            mock_services['event_bus']
        )
        game.init()
        
        initial_bullet_count = len(game.player_bullets)
        
        # Simulate shooting
        mock_services['input'].is_key_just_pressed.return_value = True
        game.update_game(0.1)
        
        # Should have created a bullet
        assert len(game.player_bullets) > initial_bullet_count
        
        # Bullet should have negative speed (going UP)
        if game.player_bullets:
            bullet = game.player_bullets[0]
            assert bullet.speed < 0, f"Player bullet speed should be negative (going up), got {bullet.speed}"
    
    def test_bullet_movement_up(self, mock_services, pygame_init):
        """Player bullets should move UP (Y decreases)."""
        game = SpaceInvadersGameModular(
            mock_services['display'],
            mock_services['input'],
            mock_services['audio'],
            mock_services['event_bus']
        )
        game.init()
        
        # Create bullet manually
        from hub.games.space_invaders.components.bullet import Bullet
        from hub.games.space_invaders.constants import PLAYER_BULLET_SPEED
        
        bullet = Bullet(game.player.x, game.player.y, PLAYER_BULLET_SPEED, is_enemy=False)
        initial_y = bullet.y
        
        # Update bullet
        bullet.update(0.1)
        
        # Y should decrease (moving up toward top of screen)
        assert bullet.y < initial_y, f"Bullet Y should decrease (was {initial_y}, now {bullet.y})"

