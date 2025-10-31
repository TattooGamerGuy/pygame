"""Enhanced asset manager with service integration."""

from typing import Dict, Optional, Tuple
import pygame
from hub.services.audio_service import AudioService
from hub.core.audio import AudioManager


class AssetManager:
    """Enhanced asset manager using services."""
    
    def __init__(self, audio_service: Optional[AudioService] = None):
        """
        Initialize asset manager.
        
        Args:
            audio_service: Optional audio service for sound loading
        """
        self.audio_service = audio_service
        self._images: Dict[str, pygame.Surface] = {}
        self._fonts: Dict[Tuple[str, int], pygame.font.Font] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self.base_path = "hub/assets"
    
    def load_image(
        self,
        filename: str,
        colorkey: Optional[int] = None,
        scale: Optional[Tuple[int, int]] = None
    ) -> pygame.Surface:
        """
        Load and cache an image.
        
        Args:
            filename: Image filename
            colorkey: Color key for transparency
            scale: Optional scale (width, height)
            
        Returns:
            Loaded surface
        """
        cache_key = f"{filename}_{colorkey}_{scale}"
        if cache_key in self._images:
            return self._images[cache_key]
        
        path = f"{self.base_path}/images/{filename}"
        try:
            image = pygame.image.load(path).convert()
            
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
            
            if scale:
                image = pygame.transform.scale(image, scale)
            
            self._images[cache_key] = image
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Return placeholder
            surface = pygame.Surface((32, 32))
            surface.fill((255, 0, 255))
            return surface
    
    def load_font(self, filename: Optional[str] = None, size: int = 24) -> pygame.font.Font:
        """
        Load and cache a font.
        
        Args:
            filename: Font filename (None for default)
            size: Font size
            
        Returns:
            Loaded font
        """
        cache_key = (filename, size)
        if cache_key in self._fonts:
            return self._fonts[cache_key]
        
        try:
            if filename:
                path = f"{self.base_path}/fonts/{filename}"
                font = pygame.font.Font(path, size)
            else:
                font = pygame.font.Font(None, size)
            
            self._fonts[cache_key] = font
            return font
        except Exception as e:
            print(f"Error loading font: {e}")
            return pygame.font.Font(None, size)
    
    def load_sound(self, filename: str) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound (delegates to audio service if available).
        
        Args:
            filename: Sound filename
            
        Returns:
            Sound object or None
        """
        if filename in self._sounds:
            return self._sounds[filename]
        
        if self.audio_service:
            path = f"{self.base_path}/sounds/{filename}"
            sound = self.audio_service.load_sound(path)
            if sound:
                self._sounds[filename] = sound
            return sound
        
        return None
    
    def clear_cache(self) -> None:
        """Clear all cached assets."""
        self._images.clear()
        self._fonts.clear()
        self._sounds.clear()

