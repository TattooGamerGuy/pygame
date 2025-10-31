"""Configuration service."""

from hub.config.settings import Settings
from hub.core.display import DisplayManager
from hub.core.audio import AudioManager
from hub.core.clock import ClockManager


class ConfigService:
    """Service for managing configuration and applying it to systems."""
    
    def __init__(self, settings: Settings):
        """
        Initialize config service.
        
        Args:
            settings: Settings instance
        """
        self.settings = settings
    
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

