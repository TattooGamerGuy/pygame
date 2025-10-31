"""Asset loading strategies."""

from typing import List, Optional, Callable
from abc import ABC, abstractmethod
from enum import Enum
import pygame


class LoadStrategy(Enum):
    """Loading strategy types."""
    SYNC = "sync"
    ASYNC = "async"
    STREAMING = "streaming"


class AssetLoader(ABC):
    """Abstract asset loader."""
    
    @abstractmethod
    def load(self, path: str) -> any:
        """
        Load an asset.
        
        Args:
            path: Asset path
            
        Returns:
            Loaded asset
        """
        pass


class SyncAssetLoader(AssetLoader):
    """Synchronous asset loader."""
    
    def load(self, path: str) -> any:
        """Load asset synchronously."""
        # Implementation depends on asset type
        # This is a placeholder - actual loading done in AssetManager
        pass


class AsyncAssetLoader(AssetLoader):
    """Asynchronous asset loader (placeholder for future implementation)."""
    
    def __init__(self, callback: Optional[Callable] = None):
        """Initialize async loader."""
        self.callback = callback
    
    def load(self, path: str) -> any:
        """Load asset asynchronously (placeholder)."""
        # Future: use threading or asyncio
        pass


class StreamingAssetLoader(AssetLoader):
    """Streaming asset loader (placeholder for future implementation)."""
    
    def load(self, path: str) -> any:
        """Load asset with streaming (placeholder)."""
        # Future: stream large assets
        pass


class AssetLoadManager:
    """Manages different asset loading strategies."""
    
    def __init__(self):
        """Initialize load manager."""
        self.strategies = {
            LoadStrategy.SYNC: SyncAssetLoader(),
            LoadStrategy.ASYNC: AsyncAssetLoader(),
            LoadStrategy.STREAMING: StreamingAssetLoader()
        }
        self.default_strategy = LoadStrategy.SYNC
    
    def set_strategy(self, strategy: LoadStrategy) -> None:
        """Set default loading strategy."""
        self.default_strategy = strategy
    
    def get_loader(self, strategy: Optional[LoadStrategy] = None) -> AssetLoader:
        """Get loader for strategy."""
        strat = strategy or self.default_strategy
        return self.strategies.get(strat, self.strategies[LoadStrategy.SYNC])

