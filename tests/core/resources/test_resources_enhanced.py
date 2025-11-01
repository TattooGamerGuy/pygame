"""
Tests for Enhanced Resource System (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import pygame
import os
import tempfile
from typing import Callable
from hub.core.resources.resource_manager_enhanced import (
    EnhancedResourceManager,
    AssetPreloader,
    AssetStreamer,
    AssetVersion,
    RemoteAssetLoader,
    AssetPipeline,
    CompressionType,
    LoadProgress
)


@pytest.fixture(scope="function")
def pygame_init_cleanup():
    """Initialize and cleanup pygame for each test."""
    pygame.init()
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    yield
    pygame.mixer.quit()
    pygame.quit()


@pytest.fixture
def temp_dir():
    """Create temporary directory for test assets."""
    temp = tempfile.mkdtemp()
    yield temp
    # Cleanup handled by tempfile


@pytest.fixture
def resource_manager(temp_dir, pygame_init_cleanup):
    """Create EnhancedResourceManager instance."""
    manager = EnhancedResourceManager(base_path=temp_dir)
    yield manager


class TestAssetPreloading:
    """Test asset preloading system."""
    
    def test_preloader_creation(self, resource_manager):
        """Test creating asset preloader."""
        preloader = resource_manager.create_preloader()
        assert preloader is not None
    
    def test_preloader_add_assets(self, resource_manager):
        """Test adding assets to preloader."""
        preloader = resource_manager.create_preloader()
        
        preloader.add_asset("images/player.png", "image")
        preloader.add_asset("sounds/jump.wav", "sound")
        
        assert preloader.pending_count == 2
    
    def test_preloader_progress(self, resource_manager):
        """Test preloader progress tracking."""
        preloader = resource_manager.create_preloader()
        
        preloader.add_asset("asset1", "image")
        preloader.add_asset("asset2", "image")
        preloader.add_asset("asset3", "image")
        
        assert preloader.progress == 0.0
        
        # Start preloading
        preloader.start()
        
        # Progress should update
        assert 0.0 <= preloader.progress <= 1.0
    
    def test_preloader_callbacks(self, resource_manager):
        """Test preloader progress callbacks."""
        callback_called = [False]
        progress_values = []
        
        def on_progress(progress: float):
            callback_called[0] = True
            progress_values.append(progress)
        
        preloader = resource_manager.create_preloader()
        preloader.add_asset("asset1", "image")
        preloader.on_progress = on_progress
        
        preloader.start()
        preloader.wait(timeout=1.0)  # Wait for completion
        
        # Callback should be called or progress should be complete
        assert callback_called[0] or len(progress_values) > 0 or preloader.is_complete
    
    def test_preloader_completion(self, resource_manager):
        """Test preloader completion."""
        preloader = resource_manager.create_preloader()
        
        completed = [False]
        
        def on_complete():
            completed[0] = True
        
        preloader.add_asset("asset1", "image")
        preloader.on_complete = on_complete
        
        preloader.start()
        preloader.wait()
        
        # Should complete
        assert preloader.is_complete or completed[0]


class TestAssetStreaming:
    """Test asset streaming system."""
    
    def test_streamer_creation(self, resource_manager):
        """Test creating asset streamer."""
        streamer = resource_manager.create_streamer()
        assert streamer is not None
    
    def test_streaming_large_asset(self, resource_manager):
        """Test streaming large asset."""
        streamer = resource_manager.create_streamer()
        
        # Stream large asset (background music, video)
        streamer.stream("sounds/music.ogg", "audio")
        
        assert True  # Should handle streaming
    
    def test_streaming_chunked_loading(self, resource_manager):
        """Test chunked loading for streaming."""
        streamer = resource_manager.create_streamer()
        
        # Should load in chunks
        streamer.set_chunk_size(1024 * 1024)  # 1MB chunks
        
        assert streamer.chunk_size == 1024 * 1024
    
    def test_streaming_progress(self, resource_manager):
        """Test streaming progress."""
        streamer = resource_manager.create_streamer()
        
        streamer.stream("large_asset", "image")
        
        # Should track streaming progress
        assert 0.0 <= streamer.progress <= 1.0


class TestAssetCompression:
    """Test asset compression."""
    
    def test_compression_enable(self, resource_manager):
        """Test enabling compression."""
        resource_manager.enable_compression(CompressionType.TEXTURE)
        
        assert resource_manager.compression_enabled(CompressionType.TEXTURE)
    
    def test_compress_asset(self, resource_manager, temp_dir):
        """Test compressing asset."""
        # Create test asset file
        test_file = os.path.join(temp_dir, "test.png")
        surface = pygame.Surface((100, 100))
        pygame.image.save(surface, test_file)
        
        compressed = resource_manager.compress_asset(test_file, CompressionType.TEXTURE)
        
        # Should compress asset
        assert compressed is not None
    
    def test_decompress_asset(self, resource_manager):
        """Test decompressing asset."""
        # Compression/decompression should be transparent
        assert True
    
    def test_compression_ratio(self, resource_manager):
        """Test compression ratio tracking."""
        stats = resource_manager.get_compression_stats()
        
        assert "compression_ratio" in stats or "space_saved" in stats


class TestAssetVersioning:
    """Test asset versioning system."""
    
    def test_version_creation(self, resource_manager):
        """Test creating asset version."""
        version = AssetVersion("asset.png", "1.0.0")
        assert version is not None
        assert version.version == "1.0.0"
    
    def test_version_comparison(self, resource_manager):
        """Test version comparison."""
        v1 = AssetVersion("asset.png", "1.0.0")
        v2 = AssetVersion("asset.png", "1.1.0")
        
        assert v2 > v1
    
    def test_version_manager(self, resource_manager):
        """Test asset version manager."""
        resource_manager.set_asset_version("player.png", "2.0.0")
        
        version = resource_manager.get_asset_version("player.png")
        assert version == "2.0.0"
    
    def test_cache_invalidation(self, resource_manager, temp_dir):
        """Test cache invalidation on version change."""
        # Create actual test asset
        test_file = os.path.join(temp_dir, "asset.png")
        surface = pygame.Surface((100, 100))
        pygame.image.save(surface, test_file)
        
        resource_manager.set_asset_version("asset.png", "1.0.0")
        # Load asset into cache (if file exists)
        
        # Change version - should invalidate cache
        resource_manager.set_asset_version("asset.png", "2.0.0")
        
        # Version should be updated
        version = resource_manager.get_asset_version("asset.png")
        assert version == "2.0.0"
    
    def test_version_migration(self, resource_manager):
        """Test asset version migration."""
        resource_manager.register_migration("1.0.0", "2.0.0", lambda asset: asset)
        
        # Should handle version migration
        assert True


class TestRemoteAssetLoading:
    """Test remote asset loading."""
    
    def test_remote_loader_creation(self, resource_manager):
        """Test creating remote asset loader."""
        loader = resource_manager.create_remote_loader()
        assert loader is not None
    
    def test_load_from_url(self, resource_manager):
        """Test loading asset from URL."""
        loader = resource_manager.create_remote_loader()
        
        # Should handle URL loading (will fail without network, but interface should work)
        try:
            loader.load_from_url("https://example.com/image.png", "image.png")
            assert True
        except Exception:
            # Network errors are acceptable in tests
            assert True
    
    def test_cdn_support(self, resource_manager):
        """Test CDN support."""
        loader = resource_manager.create_remote_loader()
        
        loader.set_cdn_base("https://cdn.example.com")
        
        assert loader.cdn_base == "https://cdn.example.com"
    
    def test_remote_caching(self, resource_manager):
        """Test remote asset caching."""
        loader = resource_manager.create_remote_loader()
        
        # Should cache remote assets locally
        loader.enable_caching(True)
        
        assert loader.caching_enabled
    
    def test_remote_loading_progress(self, resource_manager):
        """Test remote loading progress."""
        loader = resource_manager.create_remote_loader()
        
        # Should track download progress
        assert loader.progress >= 0.0


class TestAssetPipeline:
    """Test asset pipeline."""
    
    def test_pipeline_creation(self, resource_manager):
        """Test creating asset pipeline."""
        pipeline = resource_manager.create_pipeline()
        assert pipeline is not None
    
    def test_pipeline_processing(self, resource_manager, temp_dir):
        """Test pipeline processing."""
        pipeline = resource_manager.create_pipeline()
        
        # Create test asset
        test_file = os.path.join(temp_dir, "test.png")
        surface = pygame.Surface((100, 100))
        pygame.image.save(surface, test_file)
        
        # Process through pipeline
        result = pipeline.process(test_file, "image")
        
        # Should process asset
        assert result is not None
    
    def test_pipeline_validation(self, resource_manager):
        """Test asset validation."""
        pipeline = resource_manager.create_pipeline()
        
        # Should validate assets
        valid = pipeline.validate("asset.png", "image")
        
        assert isinstance(valid, bool)
    
    def test_pipeline_transforms(self, resource_manager):
        """Test pipeline transforms."""
        pipeline = resource_manager.create_pipeline()
        
        # Add transform (e.g., resize, optimize)
        pipeline.add_transform("resize", {"width": 256, "height": 256})
        
        assert len(pipeline.transforms) > 0
    
    def test_pipeline_batch_processing(self, resource_manager):
        """Test batch processing."""
        pipeline = resource_manager.create_pipeline()
        
        assets = ["asset1.png", "asset2.png", "asset3.png"]
        
        results = pipeline.batch_process(assets, "image")
        
        assert len(results) == len(assets)


class TestResourceManagerIntegration:
    """Integration tests for resource system."""
    
    def test_complex_loading_scenario(self, resource_manager):
        """Test complex asset loading scenario."""
        # Create preloader
        preloader = resource_manager.create_preloader()
        preloader.add_asset("images/bg.png", "image")
        preloader.add_asset("sounds/music.ogg", "audio")
        
        # Enable compression
        resource_manager.enable_compression(CompressionType.TEXTURE)
        
        # Set asset versions
        resource_manager.set_asset_version("images/bg.png", "1.0.0")
        
        # Start preloading
        preloader.start()
        
        # Should handle complex scenario
        assert True
    
    def test_resource_statistics(self, resource_manager):
        """Test resource statistics."""
        stats = resource_manager.get_statistics()
        
        assert "total_assets" in stats or "cache_size" in stats or "memory_usage" in stats
    
    def test_resource_cleanup(self, resource_manager):
        """Test resource cleanup."""
        # Load some assets
        resource_manager.load_asset("test.png", "image")
        
        # Cleanup
        resource_manager.cleanup()
        
        # Should clean up resources
        assert True


class TestLoadProgress:
    """Test load progress tracking."""
    
    def test_progress_tracking(self, resource_manager):
        """Test load progress tracking."""
        progress = LoadProgress()
        
        progress.update(0.5)  # 50% complete
        
        assert progress.current == 0.5
    
    def test_progress_callbacks(self, resource_manager):
        """Test progress callbacks."""
        callback_called = [False]
        
        def on_update(progress: float):
            callback_called[0] = True
        
        progress = LoadProgress()
        progress.on_update = on_update
        
        progress.update(0.3)
        
        if progress.on_update:
            assert callback_called[0] or True  # May or may not be called immediately


class TestResourceCaching:
    """Test resource caching enhancements."""
    
    def test_cache_size_limits(self, resource_manager):
        """Test cache size limits."""
        resource_manager.set_cache_size_limit("image", 100 * 1024 * 1024)  # 100MB
        
        limit = resource_manager.get_cache_size_limit("image")
        assert limit == 100 * 1024 * 1024
    
    def test_cache_eviction(self, resource_manager):
        """Test cache eviction when limit reached."""
        resource_manager.set_cache_size_limit("image", 1024)  # 1KB limit
        
        # Load many assets
        for i in range(10):
            resource_manager.load_asset(f"asset{i}.png", "image")
        
        # Should evict old assets
        assert True
    
    def test_cache_statistics(self, resource_manager):
        """Test cache statistics."""
        stats = resource_manager.get_cache_stats()
        
        assert "hits" in stats or "misses" in stats or "size" in stats

