"""Sound effect management and pooling - Modular."""

from typing import Dict, Optional, List
import pygame


class SoundPool:
    """Manages sound effects with pooling for performance."""
    
    def __init__(self, pool_size: int = 8):
        """
        Initialize sound pool.
        
        Args:
            pool_size: Number of simultaneous sound channels
        """
        self.pool_size = pool_size
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._channels: List[pygame.mixer.Channel] = []
        self._next_channel = 0
    
    def load_sound(self, name: str, filepath: str) -> bool:
        """
        Load a sound effect.
        
        Args:
            name: Sound identifier
            filepath: Path to sound file
            
        Returns:
            True if loaded successfully
        """
        try:
            sound = pygame.mixer.Sound(filepath)
            self._sounds[name] = sound
            return True
        except pygame.error as e:
            print(f"Warning: Failed to load sound '{name}': {e}")
            return False
    
    def play(self, name: str, volume: float = 1.0, loops: int = 0) -> Optional[pygame.mixer.Channel]:
        """
        Play a sound effect.
        
        Args:
            name: Sound identifier
            volume: Volume (0.0 to 1.0)
            loops: Number of loops (-1 for infinite)
            
        Returns:
            Channel object or None if failed
        """
        if name not in self._sounds:
            print(f"Warning: Sound '{name}' not loaded")
            return None
        
        sound = self._sounds[name]
        sound.set_volume(max(0.0, min(1.0, volume)))
        
        channel = sound.play(loops=loops)
        return channel
    
    def stop(self, name: Optional[str] = None) -> None:
        """
        Stop playing sound(s).
        
        Args:
            name: Sound name to stop (None stops all)
        """
        if name:
            if name in self._sounds:
                self._sounds[name].stop()
        else:
            pygame.mixer.stop()
    
    def unload(self, name: str) -> None:
        """Unload a sound effect."""
        if name in self._sounds:
            self._sounds[name].stop()
            del self._sounds[name]
    
    def cleanup(self) -> None:
        """Cleanup all sound resources."""
        pygame.mixer.stop()
        self._sounds.clear()
        self._channels.clear()

