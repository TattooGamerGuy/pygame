"""
Save service for game state management.

Manages game saves, multiple save slots, encryption, and auto-save.
"""

from typing import Dict, List, Optional, Any
import os
import json
import time
import hashlib


class SaveService:
    """Service for managing game saves."""
    
    def __init__(self):
        """Initialize save service."""
        self._save_directory: Optional[str] = None
        self._encryption_enabled = False
        self._encryption_key: Optional[str] = None
        self._auto_save_enabled = False
        self._auto_save_interval = 300.0  # 5 minutes
        self._last_auto_save: Dict[str, float] = {}  # game -> timestamp
    
    def set_save_directory(self, directory: str) -> None:
        """Set save directory."""
        self._save_directory = directory
        os.makedirs(directory, exist_ok=True)
    
    def save_game_state(
        self,
        game_name: str,
        slot_name: str,
        state_data: Dict[str, Any]
    ) -> bool:
        """
        Save game state.
        
        Args:
            game_name: Name of game
            slot_name: Save slot name
            state_data: State data to save
            
        Returns:
            True if successful
        """
        if not self._save_directory:
            return False
        
        try:
            # Create game directory
            game_dir = os.path.join(self._save_directory, game_name)
            os.makedirs(game_dir, exist_ok=True)
            
            save_path = os.path.join(game_dir, f"{slot_name}.save")
            
            save_data = {
                'game': game_name,
                'slot': slot_name,
                'state': state_data,
                'timestamp': time.time(),
                'version': '1.0'
            }
            
            # Encrypt if enabled
            if self._encryption_enabled:
                save_data = self._encrypt_data(save_data)
            
            with open(save_path, 'w') as f:
                json.dump(save_data, f)
            
            self._last_auto_save[game_name] = time.time()
            return True
        except Exception:
            return False
    
    def load_game_state(
        self,
        game_name: str,
        slot_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Load game state.
        
        Args:
            game_name: Name of game
            slot_name: Save slot name
            
        Returns:
            State data or None if not found
        """
        if not self._save_directory:
            return None
        
        try:
            save_path = os.path.join(
                self._save_directory,
                game_name,
                f"{slot_name}.save"
            )
            
            if not os.path.exists(save_path):
                return None
            
            with open(save_path, 'r') as f:
                save_data = json.load(f)
            
            # Decrypt if encrypted
            if self._encryption_enabled:
                save_data = self._decrypt_data(save_data)
            
            return save_data.get('state')
        except Exception:
            return None
    
    def list_save_slots(self, game_name: str) -> List[str]:
        """
        List all save slots for a game.
        
        Args:
            game_name: Name of game
            
        Returns:
            List of slot names
        """
        if not self._save_directory:
            return []
        
        game_dir = os.path.join(self._save_directory, game_name)
        if not os.path.exists(game_dir):
            return []
        
        slots = []
        for filename in os.listdir(game_dir):
            if filename.endswith('.save'):
                slot_name = filename[:-5]  # Remove .save extension
                slots.append(slot_name)
        
        return slots
    
    def delete_save_slot(self, game_name: str, slot_name: str) -> bool:
        """
        Delete a save slot.
        
        Args:
            game_name: Name of game
            slot_name: Save slot name
            
        Returns:
            True if successful
        """
        if not self._save_directory:
            return False
        
        try:
            save_path = os.path.join(
                self._save_directory,
                game_name,
                f"{slot_name}.save"
            )
            
            if os.path.exists(save_path):
                os.remove(save_path)
                return True
            return False
        except Exception:
            return False
    
    def enable_encryption(self, enabled: bool) -> None:
        """Enable/disable save encryption."""
        self._encryption_enabled = enabled
    
    def set_encryption_key(self, key: str) -> None:
        """Set encryption key."""
        self._encryption_key = key
    
    def _encrypt_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt data (simplified - would use proper encryption in production)."""
        # Simplified encryption - in production would use proper encryption
        if self._encryption_key:
            # For now, just mark as encrypted
            data['_encrypted'] = True
        return data
    
    def _decrypt_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt data."""
        if data.get('_encrypted'):
            data.pop('_encrypted', None)
        return data
    
    def enable_auto_save(self, enabled: bool) -> None:
        """Enable/disable auto-save."""
        self._auto_save_enabled = enabled
    
    def set_auto_save_interval(self, interval_seconds: float) -> None:
        """Set auto-save interval."""
        self._auto_save_interval = max(1.0, interval_seconds)
    
    @property
    def auto_save_enabled(self) -> bool:
        """Check if auto-save is enabled."""
        return self._auto_save_enabled
    
    def should_auto_save(self, game_name: str) -> bool:
        """Check if auto-save should trigger."""
        if not self._auto_save_enabled:
            return False
        
        last_save = self._last_auto_save.get(game_name, 0)
        return (time.time() - last_save) >= self._auto_save_interval

