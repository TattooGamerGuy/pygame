"""Background music control - Modular."""

from typing import Optional
import pygame


class MusicController:
    """Manages background music playback."""
    
    def __init__(self):
        """Initialize music controller."""
        self._current_track: Optional[str] = None
        self._volume = 1.0
        self._fading = False
    
    def load(self, filepath: str) -> bool:
        """
        Load a music file.
        
        Args:
            filepath: Path to music file
            
        Returns:
            True if loaded successfully
        """
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self._volume)
            return True
        except pygame.error as e:
            print(f"Warning: Failed to load music: {e}")
            return False
    
    def play(self, loops: int = -1, fade_ms: int = 0) -> None:
        """
        Play background music.
        
        Args:
            loops: Number of loops (-1 for infinite)
            fade_ms: Fade in duration in milliseconds
        """
        if fade_ms > 0:
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
        else:
            pygame.mixer.music.play(loops=loops)
    
    def stop(self, fade_ms: int = 0) -> None:
        """
        Stop background music.
        
        Args:
            fade_ms: Fade out duration in milliseconds
        """
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
    
    def pause(self) -> None:
        """Pause background music."""
        pygame.mixer.music.pause()
    
    def unpause(self) -> None:
        """Unpause background music."""
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume: float) -> None:
        """
        Set music volume.
        
        Args:
            volume: Volume (0.0 to 1.0)
        """
        self._volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._volume)
    
    @property
    def playing(self) -> bool:
        """Check if music is playing."""
        return pygame.mixer.music.get_busy()
    
    @property
    def paused(self) -> bool:
        """Check if music is paused."""
        return not self.playing and self._current_track is not None
    
    @property
    def volume(self) -> float:
        """Get current music volume."""
        return self._volume

