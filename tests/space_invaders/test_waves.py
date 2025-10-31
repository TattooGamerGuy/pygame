"""Test wave system with TDD approach."""

import pytest
from hub.games.space_invaders.waves.wave_manager import WaveManager
from hub.games.space_invaders.waves.wave_config import get_wave_config
from hub.games.space_invaders.constants import ENEMY_ROWS, ENEMY_COLS


class TestWaveManager:
    """Test wave manager functionality."""
    
    def test_wave_manager_initialization(self):
        """Wave manager should initialize correctly."""
        manager = WaveManager()
        
        assert manager.current_wave == 1
        assert len(manager.enemies) == 0
    
    def test_start_wave_creates_enemies(self):
        """Starting a wave should create enemies."""
        manager = WaveManager()
        enemies = manager.start_wave(1)
        
        assert len(enemies) == ENEMY_ROWS * ENEMY_COLS
        assert len(manager.get_enemies()) == ENEMY_ROWS * ENEMY_COLS
    
    def test_wave_progression(self):
        """Wave numbers should progress correctly."""
        manager = WaveManager()
        
        manager.start_wave(1)
        assert manager.get_current_wave() == 1
        
        manager.start_wave(5)
        assert manager.get_current_wave() == 5
    
    def test_wave_complete_detection(self):
        """Wave should be marked complete when all enemies destroyed."""
        manager = WaveManager()
        enemies = manager.start_wave(1)
        
        assert not manager.is_wave_complete(), "Wave should not be complete initially"
        
        # Remove all enemies
        for enemy in enemies[:]:
            manager.remove_enemy(enemy)
        
        assert manager.is_wave_complete(), "Wave should be complete when all enemies destroyed"
    
    def test_enemy_removal(self):
        """Removing enemy should update wave state."""
        manager = WaveManager()
        enemies = manager.start_wave(1)
        initial_count = len(enemies)
        
        manager.remove_enemy(enemies[0])
        
        assert len(manager.get_enemies()) == initial_count - 1


class TestWaveConfig:
    """Test wave configuration."""
    
    def test_wave_1_config(self):
        """Wave 1 should have base difficulty."""
        config = get_wave_config(1)
        
        assert config.wave_number == 1
        assert config.speed_multiplier >= 1.0
        assert config.move_interval > 0
        assert config.shoot_interval > 0
    
    def test_wave_progressive_difficulty(self):
        """Later waves should be more difficult."""
        wave1 = get_wave_config(1)
        wave5 = get_wave_config(5)
        
        assert wave5.speed_multiplier > wave1.speed_multiplier, "Wave 5 should be faster"
        assert wave5.move_interval <= wave1.move_interval, "Wave 5 should move more frequently"
        assert wave5.shoot_interval <= wave1.shoot_interval, "Wave 5 should shoot more frequently"
    
    def test_wave_enemy_types(self):
        """Enemy types should be assigned correctly by row."""
        config = get_wave_config(1)
        
        assert config.get_enemy_type_for_row(0) == 1, "Top row should be type 1"
        assert config.get_enemy_type_for_row(1) == 2, "Middle row should be type 2"
        assert config.get_enemy_type_for_row(2) == 2, "Middle row should be type 2"
        assert config.get_enemy_type_for_row(3) == 3, "Bottom row should be type 3"
        assert config.get_enemy_type_for_row(4) == 3, "Bottom row should be type 3"
    
    def test_wave_tier_system(self):
        """Wave tiers (every 5 waves) should increase difficulty."""
        wave4 = get_wave_config(4)
        wave5 = get_wave_config(5)
        wave6 = get_wave_config(6)
        
        # Wave 5 should have tier bonus
        assert wave5.speed_multiplier > wave4.speed_multiplier, "Wave 5 tier should increase speed"
        # Wave 6 should continue progression but not have as big a jump
        assert wave6.speed_multiplier >= wave5.speed_multiplier, "Wave 6 should continue progression"

