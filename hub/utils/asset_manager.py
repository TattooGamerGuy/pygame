"""Asset loading and caching manager."""

import os
from typing import Dict, Optional
import pygame


class AssetManager:
    """Manages loading and caching of game assets."""
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the asset manager.
        
        Args:
            base_path: Base path for assets directory. If None, uses hub/assets.
        """
        if base_path is None:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.join(current_dir, "..", "assets")
        
        self.base_path = os.path.abspath(base_path)
        self._images: Dict[str, pygame.Surface] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._fonts: Dict[tuple, pygame.font.Font] = {}
        
    def get_image_path(self, filename: str) -> str:
        """Get the full path to an image file."""
        return os.path.join(self.base_path, "images", filename)
    
    def get_sound_path(self, filename: str) -> str:
        """Get the full path to a sound file."""
        return os.path.join(self.base_path, "sounds", filename)
    
    def get_font_path(self, filename: str) -> str:
        """Get the full path to a font file."""
        return os.path.join(self.base_path, "fonts", filename)
    
    def load_image(self, filename: str, colorkey: Optional[int] = None, scale: Optional[tuple] = None) -> pygame.Surface:
        """
        Load and cache an image.
        
        Args:
            filename: Name of the image file
            colorkey: Color key for transparency (use -1 for top-left pixel)
            scale: Optional scale factor as (width, height)
            
        Returns:
            Loaded pygame Surface
        """
        cache_key = f"{filename}_{colorkey}_{scale}"
        if cache_key in self._images:
            return self._images[cache_key]
        
        path = self.get_image_path(filename)
        if not os.path.exists(path):
            # Return a placeholder surface if file doesn't exist
            print(f"Warning: Image not found: {path}")
            surface = pygame.Surface((32, 32))
            surface.fill((255, 0, 255))  # Magenta placeholder
            return surface
        
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
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            # Return placeholder
            surface = pygame.Surface((32, 32))
            surface.fill((255, 0, 255))
            return surface
    
    def load_sound(self, filename: str) -> Optional[pygame.mixer.Sound]:
        """
        Load and cache a sound effect.
        
        Args:
            filename: Name of the sound file
            
        Returns:
            Loaded pygame Sound object or None if loading fails
        """
        if filename in self._sounds:
            return self._sounds[filename]
        
        if not pygame.mixer.get_init():
            return None
        
        path = self.get_sound_path(filename)
        if not os.path.exists(path):
            print(f"Warning: Sound not found: {path}")
            return None
        
        try:
            sound = pygame.mixer.Sound(path)
            self._sounds[filename] = sound
            return sound
        except pygame.error as e:
            print(f"Error loading sound {path}: {e}")
            return None
    
    def load_font(self, filename: Optional[str] = None, size: int = 24) -> pygame.font.Font:
        """
        Load and cache a font.
        
        Args:
            filename: Name of the font file (None uses default)
            size: Font size
            
        Returns:
            Loaded pygame Font object
        """
        cache_key = (filename, size)
        if cache_key in self._fonts:
            return self._fonts[cache_key]
        
        try:
            if filename:
                path = self.get_font_path(filename)
                if os.path.exists(path):
                    font = pygame.font.Font(path, size)
                else:
                    print(f"Warning: Font not found: {path}, using default")
                    font = pygame.font.Font(None, size)
            else:
                font = pygame.font.Font(None, size)
            
            self._fonts[cache_key] = font
            return font
        except Exception as e:
            print(f"Error loading font: {e}")
            return pygame.font.Font(None, size)
    
    def clear_cache(self):
        """Clear all cached assets."""
        self._images.clear()
        self._sounds.clear()
        self._fonts.clear()

