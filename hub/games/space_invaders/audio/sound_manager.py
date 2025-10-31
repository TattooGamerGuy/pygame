"""Sound manager for Space Invaders 8-bit sound effects."""

from typing import Optional
import pygame
from hub.services.audio_service import AudioService


class SoundManager:
    """Manages 8-bit style sound effects for Space Invaders."""
    
    def __init__(self, audio_service: Optional[AudioService] = None):
        """
        Initialize sound manager.
        
        Args:
            audio_service: Optional audio service
        """
        self.audio_service = audio_service
        self.sounds_enabled = True
        self._generate_sounds()
    
    def _generate_sounds(self) -> None:
        """Generate programmatic 8-bit sound effects."""
        # Sound frequencies and durations for 8-bit style
        self.shoot_freq = 800
        self.explosion_freq = 200
        self.ufo_freq = 600
        
        # For now, we'll use simple pygame mixer sounds
        # In a full implementation, these would be generated programmatically
        # or loaded from files
        try:
            # Try to initialize mixer if not already
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except:
            self.sounds_enabled = False
    
    def play_shoot(self) -> None:
        """Play shoot sound effect."""
        if not self.sounds_enabled:
            return
        
        # Generate simple beep sound programmatically
        try:
            duration = 0.1
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * (1 if (i * self.shoot_freq // sample_rate) % 2 else -1)
                arr.append([wave, wave])
            sound_array = pygame.sndarray.array(arr)
            sound = pygame.sndarray.make_sound(sound_array)
            sound.play()
        except:
            pass  # Silently fail if sound generation doesn't work
    
    def play_explosion(self) -> None:
        """Play explosion sound effect."""
        if not self.sounds_enabled:
            return
        
        try:
            duration = 0.2
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                # Lower frequency, rougher sound
                freq = self.explosion_freq - (i / frames) * 100
                wave = 4096 * (1 if (i * freq // sample_rate) % 2 else -1) * (1 - i / frames)
                arr.append([int(wave), int(wave)])
            sound_array = pygame.sndarray.array(arr)
            sound = pygame.sndarray.make_sound(sound_array)
            sound.play()
        except:
            pass
    
    def play_ufo(self) -> None:
        """Play UFO sound effect."""
        if not self.sounds_enabled:
            return
        
        try:
            duration = 0.15
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                # Wobbling frequency
                freq = self.ufo_freq + 50 * (1 if (i // 100) % 2 else -1)
                wave = 4096 * (1 if (i * freq // sample_rate) % 2 else -1) * 0.7
                arr.append([int(wave), int(wave)])
            sound_array = pygame.sndarray.array(arr)
            sound = pygame.sndarray.make_sound(sound_array)
            sound.play()
        except:
            pass
    
    def play_shield_hit(self) -> None:
        """Play shield hit sound."""
        if not self.sounds_enabled:
            return
        
        try:
            duration = 0.05
            sample_rate = 22050
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 2048 * (1 if (i * 1000 // sample_rate) % 2 else -1)
                arr.append([int(wave), int(wave)])
            sound_array = pygame.sndarray.array(arr)
            sound = pygame.sndarray.make_sound(sound_array)
            sound.play()
        except:
            pass
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable sounds."""
        self.sounds_enabled = enabled

