"""Settings management with persistence."""

import json
import os
from typing import Any, Dict, Optional
from hub.config.defaults import *


class Settings:
    """Manages application settings with file persistence."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize settings.
        
        Args:
            config_file: Path to config file (defaults to ~/.gamehub_config.json)
        """
        if config_file is None:
            config_file = os.path.join(os.path.expanduser("~"), ".gamehub_config.json")
        
        self._config_file = config_file
        self._settings: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load settings from file."""
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r') as f:
                    self._settings = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load settings: {e}")
                self._settings = {}
        else:
            self._settings = {}
        self._apply_defaults()
    
    def save(self) -> None:
        """Save settings to file."""
        try:
            with open(self._config_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save settings: {e}")
    
    def _apply_defaults(self) -> None:
        """Apply default values for missing settings."""
        defaults = {
            'resolution': DEFAULT_RESOLUTION,
            'fullscreen': DEFAULT_FULLSCREEN,
            'resizable': DEFAULT_RESIZABLE,
            'target_fps': DEFAULT_TARGET_FPS,
            'master_volume': DEFAULT_MASTER_VOLUME,
        }
        
        for key, value in defaults.items():
            if key not in self._settings:
                self._settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self._settings[key] = value
    
    def has(self, key: str) -> bool:
        """Check if setting exists."""
        return key in self._settings

