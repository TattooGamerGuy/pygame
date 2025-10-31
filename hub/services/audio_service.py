"""Audio playback service."""

from typing import Optional
import pygame
import os
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

