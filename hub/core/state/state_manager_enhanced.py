"""
Enhanced state management system.

Supports save/load, state snapshots, persistence, validation, and inspection.
"""

from typing import Dict, Optional, List, Any, Callable
from dataclasses import dataclass, field
import os
import json
import time
import hashlib


@dataclass
class SaveSlot:
    """Save slot for game state."""
    name: str
    save_directory: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    _encrypted: bool = False
    
    def get_path(self) -> str:
        """Get save file path."""
        return os.path.join(self.save_directory, f"{self.name}.save")
    
    def save(self, state_data: Dict[str, Any]) -> bool:
        """
        Save state to slot.
        
        Args:
            state_data: State data to save
            
        Returns:
            True if successful
        """
        try:
            path = self.get_path()
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            save_data = {
                'state': state_data,
                'metadata': self.metadata.copy(),
                'timestamp': time.time()
            }
            
            with open(path, 'w') as f:
                json.dump(save_data, f)
            
            return True
        except Exception:
            return False
    
    def load(self) -> Optional[Dict[str, Any]]:
        """
        Load state from slot.
        
        Returns:
            State data or None if failed
        """
        try:
            path = self.get_path()
            if not os.path.exists(path):
                return None
            
            with open(path, 'r') as f:
                save_data = json.load(f)
            
            # Update metadata
            if 'metadata' in save_data:
                self.metadata.update(save_data['metadata'])
            
            return save_data.get('state')
        except Exception:
            return None
    
    def exists(self) -> bool:
        """Check if save file exists."""
        return os.path.exists(self.get_path())
    
    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value."""
        self.metadata[key] = value
    
    def get_metadata(self, key: str) -> Optional[Any]:
        """Get metadata value."""
        return self.metadata.get(key)
    
    def delete(self) -> bool:
        """Delete save file."""
        try:
            path = self.get_path()
            if os.path.exists(path):
                os.remove(path)
            return True
        except Exception:
            return False


class SaveSystem:
    """Save/load system for game state."""
    
    def __init__(self):
        """Initialize save system."""
        self._slots: Dict[str, SaveSlot] = {}
        self._save_directory: Optional[str] = None
        self._encryption_enabled = False
        self._encryption_key: Optional[str] = None
    
    def set_save_directory(self, directory: str) -> None:
        """Set save directory."""
        self._save_directory = directory
        os.makedirs(directory, exist_ok=True)
    
    def create_slot(self, name: str) -> SaveSlot:
        """Create save slot."""
        if not self._save_directory:
            # Use default directory
            self._save_directory = os.path.join(os.getcwd(), "saves")
        
        slot = SaveSlot(name, self._save_directory)
        self._slots[name] = slot
        return slot
    
    def get_slot(self, name: str) -> Optional[SaveSlot]:
        """Get save slot."""
        if name in self._slots:
            return self._slots[name]
        # Don't auto-create - return None if doesn't exist
        return None
    
    def delete_slot(self, name: str) -> bool:
        """Delete save slot."""
        if name in self._slots:
            slot = self._slots[name]
            slot.delete()
            del self._slots[name]
            return True
        return False
    
    def slot_exists(self, name: str) -> bool:
        """Check if save slot exists."""
        if name in self._slots:
            return self._slots[name].exists()
        return False
    
    @property
    def encryption_enabled(self) -> bool:
        """Check if encryption is enabled."""
        return self._encryption_enabled
    
    def enable_encryption(self, enabled: bool) -> None:
        """Enable/disable encryption."""
        self._encryption_enabled = enabled
    
    def set_encryption_key(self, key: str) -> None:
        """Set encryption key."""
        self._encryption_key = key


@dataclass
class StateSnapshot:
    """State snapshot for undo/redo."""
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    description: Optional[str] = None
    
    def copy(self) -> 'StateSnapshot':
        """Create copy of snapshot."""
        import copy
        return StateSnapshot(
            data=copy.deepcopy(self.data),
            timestamp=self.timestamp,
            description=self.description
        )


class StatePersistence:
    """State persistence across sessions."""
    
    def __init__(self):
        """Initialize persistence."""
        self._persistence_directory: Optional[str] = None
        self._enabled = False
        self._auto_save = False
        self._auto_save_interval = 60.0  # seconds
        self._last_auto_save = 0.0
        self._persisted_keys: List[str] = []
    
    def set_persistence_directory(self, directory: str) -> None:
        """Set persistence directory."""
        self._persistence_directory = directory
        os.makedirs(directory, exist_ok=True)
    
    def enable(self) -> None:
        """Enable persistence."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable persistence."""
        self._enabled = False
    
    @property
    def is_enabled(self) -> bool:
        """Check if persistence is enabled."""
        return self._enabled
    
    def persist(self, key: str, state_data: Dict[str, Any]) -> bool:
        """
        Persist state data.
        
        Args:
            key: Persistence key
            state_data: State data
            
        Returns:
            True if successful
        """
        if not self._enabled or not self._persistence_directory:
            return False
        
        try:
            path = os.path.join(self._persistence_directory, f"{key}.persist")
            with open(path, 'w') as f:
                json.dump(state_data, f)
            
            if key not in self._persisted_keys:
                self._persisted_keys.append(key)
            
            return True
        except Exception:
            return False
    
    def restore(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Restore persisted state.
        
        Args:
            key: Persistence key
            
        Returns:
            State data or None if not found
        """
        if not self._persistence_directory:
            return None
        
        try:
            path = os.path.join(self._persistence_directory, f"{key}.persist")
            if not os.path.exists(path):
                return None
            
            with open(path, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    
    def get_persisted_keys(self) -> List[str]:
        """Get list of persisted keys."""
        if not self._persistence_directory:
            return []
        
        keys = []
        for filename in os.listdir(self._persistence_directory):
            if filename.endswith('.persist'):
                keys.append(filename[:-8])  # Remove .persist extension
        
        return keys
    
    def set_auto_save(self, enabled: bool) -> None:
        """Enable/disable auto-save."""
        self._auto_save = enabled
    
    @property
    def auto_save_enabled(self) -> bool:
        """Check if auto-save is enabled."""
        return self._auto_save


class StateValidator:
    """State validation system."""
    
    def __init__(self):
        """Initialize validator."""
        self._schema: Optional[Dict[str, type]] = None
        self._required_fields: List[str] = []
        self._validation_rules: Dict[str, Callable] = {}
    
    def set_schema(self, schema: Dict[str, type]) -> None:
        """Set validation schema."""
        self._schema = schema
    
    def set_required_fields(self, fields: List[str]) -> None:
        """Set required fields."""
        self._required_fields = fields.copy()
    
    def add_validation_rule(self, field: str, rule: Callable[[Any], bool]) -> None:
        """Add validation rule for field."""
        self._validation_rules[field] = rule
    
    def validate(self, state_data: Dict[str, Any]) -> bool:
        """
        Validate state data.
        
        Args:
            state_data: State data to validate
            
        Returns:
            True if valid
        """
        # Check required fields
        for field in self._required_fields:
            if field not in state_data:
                return False
        
        # Check schema
        if self._schema:
            for field, field_type in self._schema.items():
                if field in state_data:
                    if not isinstance(state_data[field], field_type):
                        return False
        
        # Check validation rules
        for field, rule in self._validation_rules.items():
            if field in state_data:
                if not rule(state_data[field]):
                    return False
        
        return True
    
    def recover(self, invalid_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempt to recover from invalid state.
        
        Args:
            invalid_state: Invalid state data
            
        Returns:
            Recovered state
        """
        recovered = {}
        
        # Try to fix type mismatches
        if self._schema:
            for field, field_type in self._schema.items():
                if field in invalid_state:
                    value = invalid_state[field]
                    try:
                        if not isinstance(value, field_type):
                            # Try to convert
                            if field_type == int:
                                value = int(value)
                            elif field_type == float:
                                value = float(value)
                            elif field_type == str:
                                value = str(value)
                        recovered[field] = value
                    except (ValueError, TypeError):
                        # Use default based on type
                        if field_type == int:
                            recovered[field] = 0
                        elif field_type == float:
                            recovered[field] = 0.0
                        elif field_type == str:
                            recovered[field] = ""
                        elif field_type == dict:
                            recovered[field] = {}
                        elif field_type == list:
                            recovered[field] = []
                elif field in self._required_fields:
                    # Add missing required field with default
                    if field_type == int:
                        recovered[field] = 0
                    elif field_type == float:
                        recovered[field] = 0.0
                    elif field_type == str:
                        recovered[field] = ""
                    elif field_type == dict:
                        recovered[field] = {}
                    elif field_type == list:
                        recovered[field] = []
        else:
            # No schema, return as-is
            recovered = invalid_state.copy()
        
        return recovered


class StateInspector:
    """State inspection and debugging."""
    
    def __init__(self):
        """Initialize inspector."""
        self._history_enabled = False
        self._history: List[Dict[str, Any]] = []
        self._max_history = 100
    
    def enable_history(self, enabled: bool) -> None:
        """Enable/disable history tracking."""
        self._history_enabled = enabled
    
    def visualize(self, state_data: Dict[str, Any]) -> str:
        """
        Visualize state as string.
        
        Args:
            state_data: State data
            
        Returns:
            String representation
        """
        lines = []
        lines.append("State Data:")
        
        def format_value(value: Any, indent: int = 2) -> str:
            if isinstance(value, dict):
                result = "{\n"
                for k, v in value.items():
                    result += " " * indent + f"{k}: {format_value(v, indent + 2)}\n"
                result += " " * (indent - 2) + "}"
                return result
            elif isinstance(value, list):
                return "[" + ", ".join(str(v) for v in value) + "]"
            else:
                return str(value)
        
        for key, value in state_data.items():
            lines.append(f"  {key}: {format_value(value)}")
        
        return "\n".join(lines)
    
    def inspect(self) -> Dict[str, Any]:
        """
        Inspect current state.
        
        Returns:
            Inspection information
        """
        return {
            'history_enabled': self._history_enabled,
            'history_count': len(self._history),
            'max_history': self._max_history
        }
    
    def diff(self, state1: Dict[str, Any], state2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare two states.
        
        Args:
            state1: First state
            state2: Second state
            
        Returns:
            Dictionary of differences
        """
        differences = {}
        
        all_keys = set(state1.keys()) | set(state2.keys())
        
        for key in all_keys:
            val1 = state1.get(key)
            val2 = state2.get(key)
            
            if val1 != val2:
                differences[key] = {
                    'old': val1,
                    'new': val2
                }
        
        return differences
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get state history."""
        return self._history.copy()
    
    def record_state(self, state_data: Dict[str, Any]) -> None:
        """Record state in history."""
        if self._history_enabled:
            self._history.append(state_data.copy())
            if len(self._history) > self._max_history:
                self._history.pop(0)


class EnhancedStateManager:
    """Enhanced state manager with save/load, snapshots, persistence, validation."""
    
    def __init__(self):
        """Initialize enhanced state manager."""
        self._state_data: Dict[str, Any] = {}
        self._save_system: Optional[SaveSystem] = None
        self._snapshots: List[StateSnapshot] = []
        self._snapshot_history: List[StateSnapshot] = []  # For undo
        self._redo_stack: List[StateSnapshot] = []
        self._max_snapshots = 50
        self._persistence: Optional[StatePersistence] = None
        self._validator: Optional[StateValidator] = None
        self._inspector: Optional[StateInspector] = None
    
    def set_state_data(self, data: Dict[str, Any]) -> None:
        """Set state data."""
        self._state_data = data.copy()
        
        if self._inspector:
            self._inspector.record_state(data)
    
    def get_state_data(self) -> Dict[str, Any]:
        """Get state data."""
        return self._state_data.copy()
    
    def get_save_system(self) -> SaveSystem:
        """Get or create save system."""
        if self._save_system is None:
            self._save_system = SaveSystem()
        return self._save_system
    
    def create_snapshot(self, data: Optional[Dict[str, Any]] = None) -> StateSnapshot:
        """Create state snapshot."""
        snapshot_data = data if data is not None else self._state_data.copy()
        snapshot = StateSnapshot(data=snapshot_data)
        return snapshot
    
    def save_snapshot(self, description: Optional[str] = None) -> None:
        """Save current state as snapshot."""
        snapshot = self.create_snapshot()
        snapshot.description = description
        
        self._snapshot_history.append(snapshot)
        self._redo_stack.clear()  # Clear redo on new action
        
        # Limit snapshot history
        if len(self._snapshot_history) > self._max_snapshots:
            self._snapshot_history.pop(0)
    
    @property
    def snapshot_count(self) -> int:
        """Get number of snapshots."""
        return len(self._snapshot_history)
    
    def set_max_snapshots(self, max_count: int) -> None:
        """Set maximum snapshots."""
        self._max_snapshots = max(1, max_count)
        while len(self._snapshot_history) > self._max_snapshots:
            self._snapshot_history.pop(0)
    
    def undo(self) -> bool:
        """Undo to previous snapshot."""
        if len(self._snapshot_history) < 2:
            return False  # Need at least 2 snapshots to undo
        
        # Current state is last snapshot, move it to redo stack
        current = self._snapshot_history.pop()
        self._redo_stack.append(current)
        
        # Get previous snapshot
        if self._snapshot_history:
            previous = self._snapshot_history[-1]
            self._state_data = previous.data.copy()
            return True
        
        return False
    
    def redo(self) -> bool:
        """Redo to next snapshot."""
        if not self._redo_stack:
            return False
        
        next_snapshot = self._redo_stack.pop()
        self._state_data = next_snapshot.data.copy()
        self._snapshot_history.append(next_snapshot)
        
        return True
    
    def can_undo(self) -> bool:
        """Check if undo is possible."""
        return len(self._snapshot_history) >= 2
    
    def can_redo(self) -> bool:
        """Check if redo is possible."""
        return len(self._redo_stack) > 0
    
    def clear_snapshots(self) -> None:
        """Clear all snapshots."""
        self._snapshot_history.clear()
        self._redo_stack.clear()
    
    def get_persistence(self) -> StatePersistence:
        """Get or create persistence system."""
        if self._persistence is None:
            self._persistence = StatePersistence()
        return self._persistence
    
    def get_validator(self) -> StateValidator:
        """Get or create validator."""
        if self._validator is None:
            self._validator = StateValidator()
        return self._validator
    
    def get_inspector(self) -> StateInspector:
        """Get or create inspector."""
        if self._inspector is None:
            self._inspector = StateInspector()
        return self._inspector
    
    def validate_state(self) -> bool:
        """Validate current state."""
        if self._validator:
            return self._validator.validate(self._state_data)
        return True  # No validator means always valid
    
    def recover_state(self) -> None:
        """Attempt to recover from invalid state."""
        if self._validator:
            self._state_data = self._validator.recover(self._state_data)

