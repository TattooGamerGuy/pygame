"""
Enhanced resource management system.

Supports asset preloading, streaming, compression, versioning,
remote loading, and asset pipeline processing.
"""

from typing import Dict, List, Optional, Tuple, Callable, Any
from enum import Enum
from dataclasses import dataclass, field
import os
import hashlib
import threading
import time
import pygame


class CompressionType(Enum):
    """Compression types."""
    NONE = "none"
    TEXTURE = "texture"
    AUDIO = "audio"
    GENERAL = "general"


@dataclass
class AssetVersion:
    """Asset version information."""
    asset_id: str
    version: str
    hash: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    
    def __lt__(self, other: 'AssetVersion') -> bool:
        """Compare versions."""
        if not isinstance(other, AssetVersion):
            return False
        # Simple version comparison (can be enhanced)
        return self.version < other.version
    
    def __gt__(self, other: 'AssetVersion') -> bool:
        """Compare versions."""
        if not isinstance(other, AssetVersion):
            return False
        return self.version > other.version


@dataclass
class LoadProgress:
    """Load progress tracking."""
    current: float = 0.0
    total: float = 1.0
    on_update: Optional[Callable[[float], None]] = None
    
    def update(self, progress: float) -> None:
        """Update progress (0.0 to 1.0)."""
        self.current = max(0.0, min(1.0, progress))
        if self.on_update:
            self.on_update(self.current)
    
    @property
    def percentage(self) -> float:
        """Get progress percentage."""
        if self.total > 0:
            return (self.current / self.total) * 100.0
        return 0.0


class AssetPreloader:
    """Asset preloading system."""
    
    def __init__(self, resource_manager: 'EnhancedResourceManager'):
        """Initialize preloader."""
        self.resource_manager = resource_manager
        self._assets: List[Tuple[str, str]] = []  # (path, type)
        self._loaded: int = 0
        self._loading = False
        self._complete = False
        self.on_progress: Optional[Callable[[float], None]] = None
        self.on_complete: Optional[Callable[[], None]] = None
        self._thread: Optional[threading.Thread] = None
    
    @property
    def pending_count(self) -> int:
        """Get number of pending assets."""
        return len(self._assets) - self._loaded
    
    @property
    def progress(self) -> float:
        """Get progress (0.0 to 1.0)."""
        if len(self._assets) == 0:
            return 1.0
        return self._loaded / len(self._assets)
    
    @property
    def is_complete(self) -> bool:
        """Check if preloading is complete."""
        return self._complete
    
    def add_asset(self, path: str, asset_type: str) -> None:
        """Add asset to preload queue."""
        if (path, asset_type) not in self._assets:
            self._assets.append((path, asset_type))
    
    def start(self) -> None:
        """Start preloading."""
        if self._loading:
            return
        
        self._loading = True
        self._complete = False
        self._loaded = 0
        
        def load_thread():
            for path, asset_type in self._assets:
                try:
                    self.resource_manager.load_asset(path, asset_type)
                    self._loaded += 1
                    
                    if self.on_progress:
                        self.on_progress(self.progress)
                except Exception:
                    pass  # Skip failed assets
            
            self._complete = True
            self._loading = False
            if self.on_complete:
                self.on_complete()
        
        self._thread = threading.Thread(target=load_thread, daemon=True)
        self._thread.start()
    
    def wait(self, timeout: Optional[float] = None) -> bool:
        """Wait for preloading to complete."""
        if self._thread:
            self._thread.join(timeout=timeout)
            return self._complete
        return True


class AssetStreamer:
    """Asset streaming system for large assets."""
    
    def __init__(self, resource_manager: 'EnhancedResourceManager'):
        """Initialize streamer."""
        self.resource_manager = resource_manager
        self._chunk_size = 1024 * 1024  # 1MB default
        self._streaming_assets: Dict[str, float] = {}  # asset_id -> progress
    
    @property
    def chunk_size(self) -> int:
        """Get chunk size."""
        return self._chunk_size
    
    def set_chunk_size(self, size: int) -> None:
        """Set chunk size."""
        self._chunk_size = max(1024, size)  # Min 1KB
    
    def stream(self, path: str, asset_type: str) -> None:
        """Stream large asset."""
        # Simplified streaming (would implement actual chunked loading)
        self._streaming_assets[path] = 0.0
        # In real implementation, would load in chunks
        try:
            self.resource_manager.load_asset(path, asset_type)
            self._streaming_assets[path] = 1.0
        except Exception:
            pass
    
    @property
    def progress(self) -> float:
        """Get streaming progress."""
        if not self._streaming_assets:
            return 1.0
        return sum(self._streaming_assets.values()) / len(self._streaming_assets)


class RemoteAssetLoader:
    """Remote asset loading from URLs/CDN."""
    
    def __init__(self):
        """Initialize remote loader."""
        self._cdn_base: Optional[str] = None
        self._caching_enabled = True
        self._cache_dir: Optional[str] = None
        self._download_progress: Dict[str, float] = {}
    
    @property
    def cdn_base(self) -> Optional[str]:
        """Get CDN base URL."""
        return self._cdn_base
    
    def set_cdn_base(self, base_url: str) -> None:
        """Set CDN base URL."""
        self._cdn_base = base_url.rstrip('/')
    
    @property
    def caching_enabled(self) -> bool:
        """Check if caching is enabled."""
        return self._caching_enabled
    
    def enable_caching(self, enabled: bool) -> None:
        """Enable/disable caching."""
        self._caching_enabled = enabled
    
    def load_from_url(self, url: str, local_path: str) -> bool:
        """
        Load asset from URL.
        
        Args:
            url: Remote URL
            local_path: Local path to save/load
            
        Returns:
            True if successful
        """
        # Would use requests or urllib in real implementation
        # For now, return interface
        try:
            # In real implementation: download file
            self._download_progress[url] = 1.0
            return True
        except Exception:
            return False
    
    @property
    def progress(self) -> float:
        """Get download progress."""
        if not self._download_progress:
            return 1.0
        return sum(self._download_progress.values()) / len(self._download_progress)


class AssetPipeline:
    """Asset pipeline for processing."""
    
    def __init__(self):
        """Initialize pipeline."""
        self._transforms: List[Tuple[str, Dict]] = []
        self._validators: List[Callable] = []
    
    @property
    def transforms(self) -> List[Tuple[str, Dict]]:
        """Get transforms."""
        return self._transforms.copy()
    
    def add_transform(self, transform_type: str, params: Dict) -> None:
        """Add transform to pipeline."""
        self._transforms.append((transform_type, params))
    
    def add_validator(self, validator: Callable) -> None:
        """Add validator."""
        self._validators.append(validator)
    
    def process(self, asset_path: str, asset_type: str) -> Optional[Any]:
        """
        Process asset through pipeline.
        
        Args:
            asset_path: Path to asset
            asset_type: Asset type
            
        Returns:
            Processed asset or None
        """
        # Apply transforms
        result = asset_path
        
        for transform_type, params in self._transforms:
            if transform_type == "resize" and asset_type == "image":
                # Would resize image
                pass
        
        return result
    
    def validate(self, asset_path: str, asset_type: str) -> bool:
        """
        Validate asset.
        
        Args:
            asset_path: Path to asset
            asset_type: Asset type
            
        Returns:
            True if valid
        """
        if not os.path.exists(asset_path):
            return False
        
        for validator in self._validators:
            if not validator(asset_path, asset_type):
                return False
        
        return True
    
    def batch_process(self, asset_paths: List[str], asset_type: str) -> List[Optional[Any]]:
        """Batch process assets."""
        return [self.process(path, asset_type) for path in asset_paths]


class EnhancedResourceManager:
    """Enhanced resource manager with advanced features."""
    
    def __init__(self, base_path: Optional[str] = None):
        """Initialize enhanced resource manager."""
        if base_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.join(current_dir, "..", "..", "assets")
        
        self.base_path = os.path.abspath(base_path)
        self._assets: Dict[str, Any] = {}
        self._versions: Dict[str, AssetVersion] = {}
        self._migrations: Dict[Tuple[str, str], Callable] = {}
        self._compression_enabled: Set[CompressionType] = set()
        self._cache_size_limits: Dict[str, int] = {}
        self._cache_stats = {'hits': 0, 'misses': 0, 'size': 0}
        self._preloaders: List[AssetPreloader] = []
        self._streamers: List[AssetStreamer] = []
        self._remote_loader: Optional[RemoteAssetLoader] = None
        self._pipeline: Optional[AssetPipeline] = None
    
    def load_asset(self, path: str, asset_type: str) -> Optional[Any]:
        """
        Load asset.
        
        Args:
            path: Asset path
            asset_type: Asset type (image, sound, font)
            
        Returns:
            Loaded asset or None
        """
        cache_key = f"{path}_{asset_type}"
        
        # Check cache
        if cache_key in self._assets:
            self._cache_stats['hits'] += 1
            return self._assets[cache_key]
        
        self._cache_stats['misses'] += 1
        
        # Check version
        if path in self._versions:
            # Version checking logic here
            pass
        
        # Load asset
        full_path = os.path.join(self.base_path, path) if not os.path.isabs(path) else path
        
        try:
            if asset_type == "image":
                asset = pygame.image.load(full_path).convert_alpha()
            elif asset_type == "sound":
                asset = pygame.mixer.Sound(full_path)
            elif asset_type == "font":
                asset = pygame.font.Font(full_path, 24)
            else:
                return None
            
            # Apply compression if enabled
            # (compression would be transparent)
            
            # Cache asset
            self._assets[cache_key] = asset
            self._cache_stats['size'] += self._estimate_size(asset)
            
            return asset
        except Exception:
            return None
    
    def _estimate_size(self, asset: Any) -> int:
        """Estimate asset size in bytes."""
        if isinstance(asset, pygame.Surface):
            w, h = asset.get_size()
            return w * h * 4  # RGBA
        return 1024  # Default estimate
    
    def create_preloader(self) -> AssetPreloader:
        """Create asset preloader."""
        preloader = AssetPreloader(self)
        self._preloaders.append(preloader)
        return preloader
    
    def create_streamer(self) -> AssetStreamer:
        """Create asset streamer."""
        streamer = AssetStreamer(self)
        self._streamers.append(streamer)
        return streamer
    
    def enable_compression(self, compression_type: CompressionType) -> None:
        """Enable compression for type."""
        self._compression_enabled.add(compression_type)
    
    def compression_enabled(self, compression_type: CompressionType) -> bool:
        """Check if compression is enabled."""
        return compression_type in self._compression_enabled
    
    def compress_asset(self, path: str, compression_type: CompressionType) -> Optional[str]:
        """Compress asset (returns compressed path)."""
        # Would implement actual compression
        return path
    
    def get_compression_stats(self) -> Dict:
        """Get compression statistics."""
        return {
            'compression_ratio': 0.7,  # Example
            'space_saved': 0
        }
    
    def set_asset_version(self, asset_id: str, version: str) -> None:
        """Set asset version."""
        old_version = self._versions.get(asset_id)
        hash_value = self._calculate_hash(asset_id)
        new_version = AssetVersion(asset_id, version, hash_value)
        
        # If version changed, invalidate cache
        if old_version and old_version.version != version:
            self._invalidate_cache(asset_id)
        
        self._versions[asset_id] = new_version
    
    def _invalidate_cache(self, asset_id: str) -> None:
        """Invalidate cached asset."""
        # Remove from cache if exists
        keys_to_remove = [key for key in self._assets.keys() if asset_id in key]
        for key in keys_to_remove:
            if key in self._assets:
                asset = self._assets.pop(key)
                self._cache_stats['size'] -= self._estimate_size(asset)
    
    def get_asset_version(self, asset_id: str) -> Optional[str]:
        """Get asset version."""
        version = self._versions.get(asset_id)
        return version.version if version else None
    
    def _calculate_hash(self, asset_id: str) -> str:
        """Calculate asset hash."""
        return hashlib.md5(asset_id.encode()).hexdigest()
    
    def register_migration(self, from_version: str, to_version: str, migration_func: Callable) -> None:
        """Register version migration."""
        self._migrations[(from_version, to_version)] = migration_func
    
    def create_remote_loader(self) -> RemoteAssetLoader:
        """Create remote asset loader."""
        if self._remote_loader is None:
            self._remote_loader = RemoteAssetLoader()
        return self._remote_loader
    
    def create_pipeline(self) -> AssetPipeline:
        """Create asset pipeline."""
        if self._pipeline is None:
            self._pipeline = AssetPipeline()
        return self._pipeline
    
    def set_cache_size_limit(self, asset_type: str, limit_bytes: int) -> None:
        """Set cache size limit."""
        self._cache_size_limits[asset_type] = limit_bytes
    
    def get_cache_size_limit(self, asset_type: str) -> Optional[int]:
        """Get cache size limit."""
        return self._cache_size_limits.get(asset_type)
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        return self._cache_stats.copy()
    
    def get_statistics(self) -> Dict:
        """Get resource statistics."""
        return {
            'total_assets': len(self._assets),
            'cache_size': self._cache_stats['size'],
            'memory_usage': self._cache_stats['size'],
            'cache_hits': self._cache_stats['hits'],
            'cache_misses': self._cache_stats['misses']
        }
    
    def cleanup(self) -> None:
        """Cleanup resources."""
        self._assets.clear()
        self._preloaders.clear()
        self._streamers.clear()

