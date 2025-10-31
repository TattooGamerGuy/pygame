"""Audio system management."""

from typing import Optional
import pygame


class AudioManager:
    """Manages audio system initialization and configuration."""
    
    def __init__(
        self,
        frequency: int = 44100,
        size: int = -16,
        channels: int = 2,
        buffer: int = 2048
    ):
        """
        Initialize audio manager.
        
        Args:
            frequency: Audio frequency (Hz)
            size: Audio sample size (bits, negative for signed)
            channels: Number of audio channels
            buffer: Audio buffer size
        """
        self._frequency = frequency
        self._size = size
        self._channels = channels
        self._buffer = buffer
        self._initialized = False
        self._available = False
    
    def initialize(self) -> bool:
        """
        Initialize the audio system.
        
        Returns:
            True if audio initialized successfully
        """
        if self._initialized:
            return self._available
        
        try:
            pygame.mixer.pre_init(self._frequency, self._size, self._channels, self._buffer)
            pygame.mixer.init()
            self._available = pygame.mixer.get_init() is not None
            self._initialized = True
            return self._available
        except pygame.error as e:
            print(f"Warning: Audio initialization failed: {e}")
            self._available = False
            self._initialized = True
            return False
    
    def cleanup(self) -> None:
        """Cleanup audio resources."""
        if self._initialized and self._available:
            pygame.mixer.quit()
            self._initialized = False
            self._available = False
    
    @property
    def available(self) -> bool:
        """Check if audio is available."""
        return self._available
    
    @property
    def frequency(self) -> Optional[int]:
        """Get audio frequency."""
        init_info = pygame.mixer.get_init()
        return init_info[0] if init_info else None
    
    def set_volume(self, volume: float) -> None:
        """
        Set master volume.
        
        Args:
            volume: Volume (0.0 to 1.0)
        """
        if self._available:
            volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(volume)

