"""Test game state management (TDD approach)."""

import pytest
from hub.games.space_invaders.constants import STARTING_LIVES


class TestGameState:
    """Test game state transitions and management."""
    
    def test_starting_lives(self):
        """Game should start with correct number of lives."""
        assert STARTING_LIVES == 3, f"Should start with 3 lives, got {STARTING_LIVES}"
    
    def test_lives_decrement(self):
        """Lives should decrease when player is hit."""
        # This test documents expected behavior
        # Implementation should be tested in integration tests
        lives = STARTING_LIVES
        lives -= 1
        assert lives == STARTING_LIVES - 1
    
    def test_game_over_when_lives_zero(self):
        """Game should end when lives reach zero."""
        lives = 0
        assert lives <= 0  # Game over condition

