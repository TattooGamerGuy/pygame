"""Configuration service."""

from typing import Dict, List, Optional, Callable, Any
import json
import os
from hub.config.settings import Settings
from hub.core.display import DisplayManager
from hub.core.audio import AudioManager
from hub.core.timing import ClockManager


class ConfigService:
    """Service for managing configuration and applying it to systems."""
    
    def __init__(self, settings: Settings):
        """
        Initialize config service.
        
        Args:
            settings: Settings instance
        """
        self.settings = settings
        
        # Enhanced features
        self._profiles: Dict[str, Dict[str, Any]] = {}
        self._current_profile = "default"
        self._validation_rules: Dict[str, Callable[[Any], bool]] = {}
        
        # Initialize default profile
        self._profiles["default"] = {}
    
    def apply_to_display(self, display_manager: DisplayManager) -> None:
        """Apply display settings to display manager."""
        resolution = self.settings.get('resolution')
        fullscreen = self.settings.get('fullscreen', False)
        
        if resolution:
            display_manager._size = tuple(resolution)
        display_manager._fullscreen = fullscreen
    
    def apply_to_audio(self, audio_manager: AudioManager) -> None:
        """Apply audio settings to audio manager."""
        volume = self.settings.get('master_volume', 1.0)
        audio_manager.set_volume(volume)
    
    def apply_to_clock(self, clock_manager: ClockManager) -> None:
        """Apply performance settings to clock manager."""
        fps = self.settings.get('target_fps')
        if fps:
            clock_manager.set_target_fps(fps)
    
    # Enhanced features - Profile system
    def create_profile(self, profile_name: str) -> None:
        """Create a configuration profile."""
        if profile_name not in self._profiles:
            self._profiles[profile_name] = {}
    
    def list_profiles(self) -> List[str]:
        """List all configuration profiles."""
        return list(self._profiles.keys())
    
    def set_profile(self, profile_name: str) -> bool:
        """Set active configuration profile."""
        if profile_name in self._profiles:
            self._current_profile = profile_name
            # Apply profile values to settings
            profile_values = self._profiles[profile_name]
            for key, value in profile_values.items():
                self.settings.set(key, value)
            return True
        return False
    
    def get_current_profile(self) -> str:
        """Get current profile name."""
        return self._current_profile
    
    def set_profile_value(self, key: str, value: Any) -> None:
        """Set value in current profile."""
        if self._current_profile not in self._profiles:
            self.create_profile(self._current_profile)
        self._profiles[self._current_profile][key] = value
        self.settings.set(key, value)
    
    def get_profile_value(self, key: str) -> Optional[Any]:
        """Get value from current profile."""
        if self._current_profile in self._profiles:
            return self._profiles[self._current_profile].get(key)
        return None
    
    def delete_profile(self, profile_name: str) -> bool:
        """Delete a configuration profile."""
        if profile_name == "default":
            return False  # Cannot delete default
        if profile_name in self._profiles:
            del self._profiles[profile_name]
            if self._current_profile == profile_name:
                self._current_profile = "default"
                self.set_profile("default")
            return True
        return False
    
    # Validation system
    def add_validation_rule(self, key: str, rule: Callable[[Any], bool]) -> None:
        """Add validation rule for a configuration key."""
        self._validation_rules[key] = rule
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration dictionary."""
        # If no validation rules, all configs are valid
        if not self._validation_rules:
            return True
        
        for key, value in config.items():
            if key in self._validation_rules:
                try:
                    if not self._validation_rules[key](value):
                        return False
                except Exception:
                    return False
        return True
    
    # Import/Export
    def export_config(self, filepath: str) -> bool:
        """Export configuration to file."""
        try:
            data = {
                'profiles': self._profiles,
                'current_profile': self._current_profile
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def import_config(self, filepath: str) -> bool:
        """Import configuration from file."""
        try:
            if not os.path.exists(filepath):
                return False
            with open(filepath, 'r') as f:
                data = json.load(f)
            self._profiles = data.get('profiles', {})
            current = data.get('current_profile', 'default')
            if current in self._profiles:
                self.set_profile(current)
            return True
        except Exception:
            return False

