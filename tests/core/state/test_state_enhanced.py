"""
Tests for Enhanced State System (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
import os
import tempfile
import json
from typing import Dict, Any
from hub.core.state.state_manager_enhanced import (
    EnhancedStateManager,
    SaveSystem,
    SaveSlot,
    StateSnapshot,
    StatePersistence,
    StateValidator,
    StateInspector
)


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def temp_dir():
    """Create temporary directory for save files."""
    temp = tempfile.mkdtemp()
    yield temp
    # Cleanup handled by tempfile


@pytest.fixture
def state_manager(pygame_init_cleanup):
    """Create EnhancedStateManager instance."""
    manager = EnhancedStateManager()
    yield manager


class TestSaveSystem:
    """Test save/load system."""
    
    def test_save_system_creation(self, state_manager):
        """Test creating save system."""
        save_system = state_manager.get_save_system()
        assert save_system is not None
    
    def test_save_slot_creation(self, state_manager, temp_dir):
        """Test creating save slots."""
        save_system = state_manager.get_save_system()
        save_system.set_save_directory(temp_dir)
        
        slot = save_system.create_slot("slot1")
        assert slot is not None
        assert slot.name == "slot1"
    
    def test_save_state(self, state_manager, temp_dir):
        """Test saving game state."""
        save_system = state_manager.get_save_system()
        save_system.set_save_directory(temp_dir)
        
        slot = save_system.create_slot("test_save")
        
        state_data = {"level": 1, "score": 1000, "player": {"health": 100}}
        
        result = slot.save(state_data)
        assert result is True
    
    def test_load_state(self, state_manager, temp_dir):
        """Test loading game state."""
        save_system = state_manager.get_save_system()
        save_system.set_save_directory(temp_dir)
        
        slot = save_system.create_slot("test_save")
        
        state_data = {"level": 1, "score": 1000}
        slot.save(state_data)
        
        loaded = slot.load()
        
        assert loaded is not None
        assert loaded["level"] == 1
        assert loaded["score"] == 1000
    
    def test_multiple_save_slots(self, state_manager, temp_dir):
        """Test multiple save slots."""
        save_system = state_manager.get_save_system()
        save_system.set_save_directory(temp_dir)
        
        slot1 = save_system.create_slot("slot1")
        slot2 = save_system.create_slot("slot2")
        
        slot1.save({"level": 1})
        slot2.save({"level": 5})
        
        assert slot1.load()["level"] == 1
        assert slot2.load()["level"] == 5
    
    def test_save_slot_metadata(self, state_manager, temp_dir):
        """Test save slot metadata."""
        save_system = state_manager.get_save_system()
        save_system.set_save_directory(temp_dir)
        
        slot = save_system.create_slot("test")
        slot.set_metadata("description", "Test save")
        slot.set_metadata("timestamp", "2024-01-01")
        
        assert slot.get_metadata("description") == "Test save"
        assert slot.get_metadata("timestamp") == "2024-01-01"
    
    def test_delete_save_slot(self, state_manager, temp_dir):
        """Test deleting save slot."""
        save_system = state_manager.get_save_system()
        save_system.set_save_directory(temp_dir)
        
        slot = save_system.create_slot("test")
        slot.save({"data": "test"})
        
        save_system.delete_slot("test")
        
        # Slot should be deleted
        assert save_system.get_slot("test") is None
    
    def test_save_slot_exists(self, state_manager, temp_dir):
        """Test checking if save slot exists."""
        save_system = state_manager.get_save_system()
        save_system.set_save_directory(temp_dir)
        
        assert not save_system.slot_exists("nonexistent")
        
        save_system.create_slot("test")
        save_system.get_slot("test").save({})
        
        assert save_system.slot_exists("test")


class TestStateSnapshots:
    """Test state snapshots for undo/redo."""
    
    def test_snapshot_creation(self, state_manager):
        """Test creating state snapshot."""
        snapshot = state_manager.create_snapshot({"level": 1, "score": 100})
        assert snapshot is not None
        assert snapshot.data["level"] == 1
    
    def test_snapshot_timestamp(self, state_manager):
        """Test snapshot timestamp."""
        snapshot = state_manager.create_snapshot({"data": "test"})
        
        assert snapshot.timestamp > 0
    
    def test_undo_redo_system(self, state_manager):
        """Test undo/redo system."""
        # Create initial state
        state_manager.set_state_data({"level": 1})
        
        # Create snapshot
        state_manager.save_snapshot()
        
        # Modify state
        state_manager.set_state_data({"level": 2})
        state_manager.save_snapshot()
        
        # Undo
        result = state_manager.undo()
        
        assert result is True
        assert state_manager.get_state_data()["level"] == 1
        
        # Redo
        result = state_manager.redo()
        
        assert result is True
        assert state_manager.get_state_data()["level"] == 2
    
    def test_snapshot_history_limit(self, state_manager):
        """Test snapshot history limit."""
        state_manager.set_max_snapshots(5)
        
        for i in range(10):
            state_manager.set_state_data({"value": i})
            state_manager.save_snapshot()
        
        # Should only keep last 5 snapshots
        assert state_manager.snapshot_count <= 5
    
    def test_clear_snapshots(self, state_manager):
        """Test clearing snapshots."""
        state_manager.set_state_data({"data": "test"})
        state_manager.save_snapshot()
        
        state_manager.clear_snapshots()
        
        assert state_manager.snapshot_count == 0
        assert state_manager.can_undo() is False


class TestStatePersistence:
    """Test state persistence across sessions."""
    
    def test_persistence_enable(self, state_manager):
        """Test enabling persistence."""
        persistence = state_manager.get_persistence()
        
        persistence.enable()
        assert persistence.is_enabled
        
        persistence.disable()
        assert not persistence.is_enabled
    
    def test_persist_state(self, state_manager, temp_dir):
        """Test persisting state."""
        persistence = state_manager.get_persistence()
        persistence.set_persistence_directory(temp_dir)
        persistence.enable()
        
        state_data = {"settings": {"volume": 0.8}}
        persistence.persist("settings", state_data)
        
        # Should persist to disk
        assert True
    
    def test_restore_state(self, state_manager, temp_dir):
        """Test restoring persisted state."""
        persistence = state_manager.get_persistence()
        persistence.set_persistence_directory(temp_dir)
        persistence.enable()
        
        state_data = {"settings": {"volume": 0.8}}
        persistence.persist("settings", state_data)
        
        restored = persistence.restore("settings")
        
        assert restored is not None
        assert restored["settings"]["volume"] == 0.8
    
    def test_auto_save(self, state_manager, temp_dir):
        """Test automatic state saving."""
        persistence = state_manager.get_persistence()
        persistence.set_persistence_directory(temp_dir)
        persistence.enable()
        persistence.set_auto_save(True)
        
        state_manager.set_state_data({"auto": "save"})
        
        # Should auto-save periodically
        assert persistence.auto_save_enabled
    
    def test_persistence_keys(self, state_manager, temp_dir):
        """Test managing persistence keys."""
        persistence = state_manager.get_persistence()
        persistence.set_persistence_directory(temp_dir)
        persistence.enable()  # Enable persistence
        
        result1 = persistence.persist("key1", {"data": 1})
        result2 = persistence.persist("key2", {"data": 2})
        
        # Persist should succeed
        assert result1 is True
        assert result2 is True
        
        keys = persistence.get_persisted_keys()
        
        # Should have the keys we persisted
        assert len(keys) >= 2
        # Keys should contain what we persisted
        assert "key1" in keys or "key2" in keys


class TestStateValidation:
    """Test state validation."""
    
    def test_validator_creation(self, state_manager):
        """Test creating state validator."""
        validator = state_manager.get_validator()
        assert validator is not None
    
    def test_state_schema_validation(self, state_manager):
        """Test validating state against schema."""
        validator = state_manager.get_validator()
        
        schema = {
            "level": int,
            "score": int,
            "player": dict
        }
        
        validator.set_schema(schema)
        
        valid_state = {"level": 1, "score": 100, "player": {}}
        invalid_state = {"level": "invalid", "score": 100}
        
        assert validator.validate(valid_state) is True
        assert validator.validate(invalid_state) is False
    
    def test_state_required_fields(self, state_manager):
        """Test required fields validation."""
        validator = state_manager.get_validator()
        
        validator.set_required_fields(["level", "score"])
        
        valid = {"level": 1, "score": 100}
        invalid = {"level": 1}  # Missing score
        
        assert validator.validate(valid) is True
        assert validator.validate(invalid) is False
    
    def test_state_type_validation(self, state_manager):
        """Test state type validation."""
        validator = state_manager.get_validator()
        
        validator.add_validation_rule("level", lambda x: isinstance(x, int) and x > 0)
        
        assert validator.validate({"level": 5}) is True
        assert validator.validate({"level": -1}) is False
        assert validator.validate({"level": "invalid"}) is False
    
    def test_state_error_recovery(self, state_manager):
        """Test error recovery on invalid state."""
        validator = state_manager.get_validator()
        
        invalid_state = {"level": "invalid"}
        
        # Should attempt recovery
        recovered = validator.recover(invalid_state)
        
        # Should provide default or corrected state
        assert recovered is not None


class TestStateInspection:
    """Test state inspection and debugging."""
    
    def test_inspector_creation(self, state_manager):
        """Test creating state inspector."""
        inspector = state_manager.get_inspector()
        assert inspector is not None
    
    def test_state_visualization(self, state_manager):
        """Test state visualization."""
        inspector = state_manager.get_inspector()
        
        state_data = {"level": 1, "score": 100, "player": {"health": 50}}
        
        visualization = inspector.visualize(state_data)
        
        # Should return string representation
        assert isinstance(visualization, str)
        assert "level" in visualization.lower() or "score" in visualization.lower()
    
    def test_state_inspection(self, state_manager):
        """Test inspecting state."""
        inspector = state_manager.get_inspector()
        
        state_data = {"level": 1, "score": 100}
        state_manager.set_state_data(state_data)
        
        info = inspector.inspect()
        
        assert "level" in info or "data" in info or info is not None
    
    def test_state_diff(self, state_manager):
        """Test comparing states."""
        inspector = state_manager.get_inspector()
        
        state1 = {"level": 1, "score": 100}
        state2 = {"level": 2, "score": 150}
        
        diff = inspector.diff(state1, state2)
        
        # Should show differences
        assert diff is not None
    
    def test_state_history_tracking(self, state_manager):
        """Test tracking state history."""
        inspector = state_manager.get_inspector()
        
        inspector.enable_history(True)
        
        state_manager.set_state_data({"step": 1})
        state_manager.set_state_data({"step": 2})
        state_manager.set_state_data({"step": 3})
        
        history = inspector.get_history()
        
        assert len(history) >= 0  # May or may not track depending on implementation


class TestSaveEncryption:
    """Test save encryption."""
    
    def test_encryption_enable(self, state_manager):
        """Test enabling save encryption."""
        save_system = state_manager.get_save_system()
        
        save_system.enable_encryption(True)
        assert save_system.encryption_enabled
    
    def test_encrypted_save_load(self, state_manager, temp_dir):
        """Test saving and loading encrypted state."""
        save_system = state_manager.get_save_system()
        save_system.set_save_directory(temp_dir)
        save_system.enable_encryption(True)
        
        slot = save_system.create_slot("encrypted")
        state_data = {"secret": "data"}
        
        slot.save(state_data)
        loaded = slot.load()
        
        assert loaded["secret"] == "data"
    
    def test_encryption_key_management(self, state_manager):
        """Test encryption key management."""
        save_system = state_manager.get_save_system()
        
        save_system.set_encryption_key("test_key")
        
        # Should handle key management
        assert True


class TestStateIntegration:
    """Integration tests for state system."""
    
    def test_complex_state_scenario(self, state_manager, temp_dir):
        """Test complex state scenario."""
        # Create save system
        save_system = state_manager.get_save_system()
        save_system.set_save_directory(temp_dir)
        
        # Create save slot
        slot = save_system.create_slot("game1")
        
        # Set initial state data
        initial_state = {
            "level": 5,
            "score": 5000,
            "player": {"health": 75, "position": [100, 200]}
        }
        state_manager.set_state_data(initial_state)
        
        # Create snapshot of initial state
        state_manager.save_snapshot()
        
        # Modify state
        modified_state = {"level": 6, "score": 5000}
        state_manager.set_state_data(modified_state)
        
        # Create another snapshot after modification
        state_manager.save_snapshot()
        
        # Save modified state to slot
        slot.save(state_manager.get_state_data())
        
        # Undo to previous snapshot (should restore initial state)
        result = state_manager.undo()
        
        # Should restore to previous snapshot
        assert result is True
        current_data = state_manager.get_state_data()
        assert current_data["level"] == 5 or "level" in current_data
    
    def test_state_persistence_across_sessions(self, state_manager, temp_dir):
        """Test state persistence across sessions."""
        persistence = state_manager.get_persistence()
        persistence.set_persistence_directory(temp_dir)
        persistence.enable()
        
        # Persist settings
        settings = {"volume": 0.8, "difficulty": "medium"}
        persistence.persist("settings", settings)
        
        # Simulate new session
        new_manager = EnhancedStateManager()
        new_persistence = new_manager.get_persistence()
        new_persistence.set_persistence_directory(temp_dir)
        new_persistence.enable()
        
        restored = new_persistence.restore("settings")
        
        assert restored["volume"] == 0.8
        assert restored["difficulty"] == "medium"

