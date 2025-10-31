"""Central resource coordinator - Modular."""

from typing import Dict, Optional
from hub.core.resources.asset_loader import AssetLoader
from hub.core.resources.cache import Cache


class ResourceManager:
    """Manages all game resources."""
    
    def __init__(self):
        """Initialize resource manager."""
        self.loader = AssetLoader()
        self.cache = Cache()
        self._resources: Dict[str, any] = {}
    
    def load_image(self, name: str, filepath: str) -> bool:
        """
        Load an image resource.
        
        Args:
            name: Resource name/identifier
            filepath: Path to image file
            
        Returns:
            True if loaded successfully
        """
        # Check cache first
        if name in self.cache:
            return True
        
        # Load new resource
        resource = self.loader.load_image(filepath)
        if resource:
            self._resources[name] = resource
            self.cache.add(name, resource)
            return True
        return False
    
    def load_sound(self, name: str, filepath: str) -> bool:
        """
        Load a sound resource.
        
        Args:
            name: Resource name/identifier
            filepath: Path to sound file
            
        Returns:
            True if loaded successfully
        """
        if name in self.cache:
            return True
        
        resource = self.loader.load_sound(filepath)
        if resource:
            self._resources[name] = resource
            self.cache.add(name, resource)
            return True
        return False
    
    def load_font(self, name: str, filepath: str, size: int = 24) -> bool:
        """
        Load a font resource.
        
        Args:
            name: Resource name/identifier
            filepath: Path to font file
            size: Font size
            
        Returns:
            True if loaded successfully
        """
        cache_key = f"{name}_{size}"
        if cache_key in self.cache:
            return True
        
        resource = self.loader.load_font(filepath, size)
        if resource:
            self._resources[cache_key] = resource
            self.cache.add(cache_key, resource)
            return True
        return False
    
    def get(self, name: str) -> Optional[any]:
        """
        Get a resource by name.
        
        Args:
            name: Resource name/identifier
            
        Returns:
            Resource object or None
        """
        return self._resources.get(name) or self.cache.get(name)
    
    def unload(self, name: str) -> None:
        """
        Unload a resource.
        
        Args:
            name: Resource name/identifier
        """
        if name in self._resources:
            del self._resources[name]
        self.cache.remove(name)
    
    def cleanup(self) -> None:
        """Cleanup all resources."""
        self._resources.clear()
        self.cache.clear()

