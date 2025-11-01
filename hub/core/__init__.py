"""Core engine modules for the game hub - Fully Modular."""

# Display system
from hub.core.display import DisplayManager, Camera, Viewport

# Audio system
from hub.core.audio import AudioManager, SoundPool, MusicController

# Timing system
from hub.core.timing import ClockManager, FixedTimestep, Timer

# Input system
from hub.core.input import InputManager, Keyboard, Mouse, Joystick

# Rendering system
from hub.core.rendering import Renderer, SpriteBatch, LayerManager

# Resource system
# Resources imported separately if needed
# from hub.core.resources import ResourceManager, AssetLoader, Cache

# Event system
from hub.core.events import (
    EventBus,
    GameEvent,
    GameStartEvent,
    GameEndEvent,
    SceneChangeEvent,
    QuitEvent
)

# State system
from hub.core.state import StateManager, GameState

# Debug system
from hub.core.debug import Profiler, DebugOverlay

# Engine
from hub.core.engine import GameEngine

__all__ = [
    # Display
    'DisplayManager',
    'Camera',
    'Viewport',
    # Audio
    'AudioManager',
    'SoundPool',
    'MusicController',
    # Timing
    'ClockManager',
    'FixedTimestep',
    'Timer',
    # Input
    'InputManager',
    'Keyboard',
    'Mouse',
    'Joystick',
    # Rendering
    'Renderer',
    'SpriteBatch',
    'LayerManager',
    # Resources
    'ResourceManager',
    'AssetLoader',
    'Cache',
    # Events
    'EventBus',
    'GameEvent',
    'GameStartEvent',
    'GameEndEvent',
    'SceneChangeEvent',
    'QuitEvent',
    # State
    'StateManager',
    'GameState',
    # Debug
    'Profiler',
    'DebugOverlay',
    # Engine
    'GameEngine',
]
