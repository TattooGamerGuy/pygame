"""Audio playback service."""

from typing import Optional, Dict
import pygame
import os
import json
from hub.core.audio import AudioManager


class AudioService:
    """Service for playing sounds and music."""
    
    def __init__(self, audio_manager: AudioManager):
        """
        Initialize audio service.
        
        Args:
            audio_manager: Audio manager instance
        """
        self.audio_manager = audio_manager
        self._sounds: dict = {}
        self._music_volume = 1.0
        self._sound_volume = 1.0
        
        # Enhanced features
        self._sound_priorities: Dict[str, int] = {}
        self._ducking_enabled = False
        self._ducking_target = "music"
        self._ducking_amount = 0.5
        self._audio_groups: Dict[str, float] = {}
        self._max_channels = 8
    
    def load_sound(self, filepath: str, name: Optional[str] = None) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound effect.
        
        Args:
            filepath: Path to sound file
            name: Optional name to store sound under
            
        Returns:
            Loaded sound object or None
        """
        if not self.audio_manager.available:
            return None
        
        try:
            sound = pygame.mixer.Sound(filepath)
            if name:
                self._sounds[name] = sound
            return sound
        except Exception as e:
            print(f"Error loading sound {filepath}: {e}")
            return None
    
    def play_sound(self, sound_or_name: str) -> None:
        """
        Play a sound effect.
        
        Args:
            sound_or_name: Sound object or name of loaded sound
        """
        if not self.audio_manager.available:
            return
        
        sound = None
        if isinstance(sound_or_name, str):
            sound = self._sounds.get(sound_or_name)
        else:
            sound = sound_or_name
        
        if sound:
            sound.set_volume(self._sound_volume)
            sound.play()
    
    def play_music(self, filepath: str, loops: int = -1) -> None:
        """
        Play background music.
        
        Args:
            filepath: Path to music file
            loops: Number of loops (-1 for infinite)
        """
        if not self.audio_manager.available:
            return
        
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self._music_volume)
            pygame.mixer.music.play(loops)
        except Exception as e:
            print(f"Error playing music {filepath}: {e}")
    
    def stop_music(self) -> None:
        """Stop background music."""
        if self.audio_manager.available:
            pygame.mixer.music.stop()
    
    def set_music_volume(self, volume: float) -> None:
        """Set music volume (0.0 to 1.0)."""
        self._music_volume = max(0.0, min(1.0, volume))
        if self.audio_manager.available:
            pygame.mixer.music.set_volume(self._music_volume)
    
    def set_sound_volume(self, volume: float) -> None:
        """Set sound effect volume (0.0 to 1.0)."""
        self._sound_volume = max(0.0, min(1.0, volume))
    
    # Enhanced features
    def set_sound_priority(self, sound_name: str, priority: int) -> None:
        """Set sound priority (higher = more important)."""
        self._sound_priorities[sound_name] = priority
    
    def get_sound_priority(self, sound_name: str) -> int:
        """Get sound priority."""
        return self._sound_priorities.get(sound_name, 5)
    
    def enable_ducking(self, enabled: bool) -> None:
        """Enable/disable audio ducking."""
        self._ducking_enabled = enabled
    
    @property
    def ducking_enabled(self) -> bool:
        """Check if ducking is enabled."""
        return self._ducking_enabled
    
    def set_ducking_target(self, target: str) -> None:
        """Set ducking target (e.g., 'music')."""
        self._ducking_target = target
    
    def set_ducking_amount(self, amount: float) -> None:
        """Set ducking amount (0.0 to 1.0)."""
        self._ducking_amount = max(0.0, min(1.0, amount))
    
    def get_ducking_amount(self) -> float:
        """Get ducking amount."""
        return self._ducking_amount
    
    def create_audio_group(self, group_name: str) -> None:
        """Create an audio group."""
        self._audio_groups[group_name] = 1.0
    
    def set_group_volume(self, group_name: str, volume: float) -> None:
        """Set audio group volume."""
        if group_name in self._audio_groups:
            self._audio_groups[group_name] = max(0.0, min(1.0, volume))
    
    def get_group_volume(self, group_name: str) -> float:
        """Get audio group volume."""
        return self._audio_groups.get(group_name, 1.0)
    
    def set_max_channels(self, max_channels: int) -> None:
        """Set maximum number of audio channels."""
        self._max_channels = max(1, max_channels)
        pygame.mixer.set_num_channels(self._max_channels)
    
    def get_max_channels(self) -> int:
        """Get maximum number of audio channels."""
        return self._max_channels
    
    def save_settings(self, filepath: str) -> bool:
        """Save audio settings."""
        try:
            data = {
                'music_volume': self._music_volume,
                'sound_volume': self._sound_volume,
                'sound_priorities': self._sound_priorities,
                'ducking_enabled': self._ducking_enabled,
                'ducking_target': self._ducking_target,
                'ducking_amount': self._ducking_amount,
                'audio_groups': self._audio_groups,
                'max_channels': self._max_channels
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_settings(self, filepath: str) -> bool:
        """Load audio settings."""
        try:
            if not os.path.exists(filepath):
                return False
            with open(filepath, 'r') as f:
                data = json.load(f)
            self._music_volume = data.get('music_volume', 1.0)
            self._sound_volume = data.get('sound_volume', 1.0)
            self._sound_priorities = data.get('sound_priorities', {})
            self._ducking_enabled = data.get('ducking_enabled', False)
            self._ducking_target = data.get('ducking_target', 'music')
            self._ducking_amount = data.get('ducking_amount', 0.5)
            self._audio_groups = data.get('audio_groups', {})
            self._max_channels = data.get('max_channels', 8)
            # Apply settings
            self.set_music_volume(self._music_volume)
            self.set_sound_volume(self._sound_volume)
            self.set_max_channels(self._max_channels)
            return True
        except Exception:
            return False

