"""Resource caching system - Modular."""

from typing import Dict, Optional, Any, OrderedDict
from collections import OrderedDict as OD


class Cache:
    """LRU cache for game resources."""
    
    def __init__(self, max_size: int = 100):
        """
        Initialize cache.
        
        Args:
            max_size: Maximum number of cached items
        """
        self.max_size = max_size
        self._cache: OrderedDict[str, Any] = OD()
    
    def add(self, key: str, value: Any) -> None:
        """
        Add item to cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        # Remove if already exists (will move to end)
        if key in self._cache:
            del self._cache[key]
        
        # Add to end
        self._cache[key] = value
        
        # Remove oldest if over limit
        while len(self._cache) > self.max_size:
            self._cache.popitem(last=False)
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if key in self._cache:
            # Move to end (mark as recently used)
            value = self._cache.pop(key)
            self._cache[key] = value
            return value
        return None
    
    def remove(self, key: str) -> None:
        """
        Remove item from cache.
        
        Args:
            key: Cache key
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
    
    def __contains__(self, key: str) -> bool:
        """Check if key is in cache."""
        return key in self._cache
    
    def __len__(self) -> int:
        """Get cache size."""
        return len(self._cache)

