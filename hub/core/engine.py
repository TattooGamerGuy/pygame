"""Main game engine orchestrator."""

from typing import Optional
import pygame
from hub.core.display.display_manager import DisplayManager
from hub.core.audio.audio_manager import AudioManager
from hub.core.timing.clock_manager import ClockManager


class GameEngine:
    """Main game engine that orchestrates all systems."""
    
    def __init__(
        self,
        display_manager: Optional[DisplayManager] = None,
        audio_manager: Optional[AudioManager] = None,
        clock_manager: Optional[ClockManager] = None
    ):
        """
        Initialize game engine.
        
        Args:
            display_manager: Display manager instance (creates default if None)
            audio_manager: Audio manager instance (creates default if None)
            clock_manager: Clock manager instance (creates default if None)
        """
        self.display = display_manager or DisplayManager()
        self.audio = audio_manager or AudioManager()
        self.clock = clock_manager or ClockManager()
        
        self._initialized = False
        self._running = False
    
    def initialize(self) -> None:
        """Initialize all engine systems."""
        if self._initialized:
            return
        
        pygame.init()
        self.display.initialize()
        self.audio.initialize()
        self.clock.reset()
        self._initialized = True
    
    def cleanup(self) -> None:
        """Cleanup all engine systems."""
        if self._initialized:
            self.audio.cleanup()
            self.display.cleanup()
            pygame.quit()
            self._initialized = False
    
    @property
    def running(self) -> bool:
        """Check if engine is running."""
        return self._running
    
    @running.setter
    def running(self, value: bool) -> None:
        """Set running state."""
        self._running = value
    
    def tick(self) -> float:
        """
        Advance the engine clock.
        
        Returns:
            Delta time in seconds
        """
        return self.clock.tick()

