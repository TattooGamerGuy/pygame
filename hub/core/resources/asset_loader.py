"""Asset loading (images, sounds, fonts) - Modular."""

from typing import Optional
import pygame


class AssetLoader:
    """Loads game assets."""
    
    def __init__(self):
        """Initialize asset loader."""
        pass
    
    def load_image(self, filepath: str) -> Optional[pygame.Surface]:
        """
        Load an image file.
        
        Args:
            filepath: Path to image file
            
        Returns:
            pygame Surface or None if failed
        """
        try:
            return pygame.image.load(filepath).convert_alpha()
        except pygame.error as e:
            print(f"Warning: Failed to load image '{filepath}': {e}")
            return None
    
    def load_sound(self, filepath: str) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound file.
        
        Args:
            filepath: Path to sound file
            
        Returns:
            pygame Sound or None if failed
        """
        try:
            return pygame.mixer.Sound(filepath)
        except pygame.error as e:
            print(f"Warning: Failed to load sound '{filepath}': {e}")
            return None
    
    def load_font(self, filepath: str, size: int = 24) -> Optional[pygame.font.Font]:
        """
        Load a font file.
        
        Args:
            filepath: Path to font file
            size: Font size
            
        Returns:
            pygame Font or None if failed
        """
        try:
            return pygame.font.Font(filepath, size)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Failed to load font '{filepath}': {e}")
            return None
    
    def load_music(self, filepath: str) -> bool:
        """
        Load a music file.
        
        Args:
            filepath: Path to music file
            
        Returns:
            True if loaded successfully
        """
        try:
            pygame.mixer.music.load(filepath)
            return True
        except pygame.error as e:
            print(f"Warning: Failed to load music '{filepath}': {e}")
            return False

