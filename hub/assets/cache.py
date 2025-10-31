"""Asset caching with LRU eviction."""

from typing import Dict, Optional, Any
from collections import OrderedDict


class LRUCache:
    """LRU (Least Recently Used) cache for assets."""
    
    def __init__(self, max_size: int = 100):
        """
        Initialize LRU cache.
        
        Args:
            max_size: Maximum number of items in cache
        """
        self.max_size = max_size
        self.cache: OrderedDict[str, Any] = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached item or None
        """
        if key not in self.cache:
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: str, value: Any) -> None:
        """
        Put item in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        if key in self.cache:
            # Update existing
            self.cache.move_to_end(key)
        else:
            # Add new
            if len(self.cache) >= self.max_size:
                # Remove least recently used (first item)
                self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def remove(self, key: str) -> bool:
        """
        Remove item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if removed, False if not found
        """
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all items from cache."""
        self.cache.clear()
    
    def size(self) -> int:
        """Get current cache size."""
        return len(self.cache)


class AssetCache:
    """Asset-specific cache manager."""
    
    def __init__(self, max_images: int = 50, max_fonts: int = 20, max_sounds: int = 30):
        """
        Initialize asset cache.
        
        Args:
            max_images: Maximum cached images
            max_fonts: Maximum cached fonts
            max_sounds: Maximum cached sounds
        """
        self.image_cache = LRUCache(max_images)
        self.font_cache = LRUCache(max_fonts)
        self.sound_cache = LRUCache(max_sounds)
    
    def get_image(self, key: str) -> Optional[Any]:
        """Get image from cache."""
        return self.image_cache.get(key)
    
    def put_image(self, key: str, value: Any) -> None:
        """Put image in cache."""
        self.image_cache.put(key, value)
    
    def get_font(self, key: str) -> Optional[Any]:
        """Get font from cache."""
        return self.font_cache.get(key)
    
    def put_font(self, key: str, value: Any) -> None:
        """Put font in cache."""
        self.font_cache.put(key, value)
    
    def get_sound(self, key: str) -> Optional[Any]:
        """Get sound from cache."""
        return self.sound_cache.get(key)
    
    def put_sound(self, key: str, value: Any) -> None:
        """Put sound in cache."""
        self.sound_cache.put(key, value)
    
    def clear_all(self) -> None:
        """Clear all caches."""
        self.image_cache.clear()
        self.font_cache.clear()
        self.sound_cache.clear()

