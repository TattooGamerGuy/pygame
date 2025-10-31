"""Default configuration values and constants."""

from typing import Tuple

# Display defaults
DEFAULT_RESOLUTION: Tuple[int, int] = (1280, 720)
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
SCREEN_SIZE: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
DEFAULT_WINDOW_TITLE: str = "8-Bit Game Hub"
DEFAULT_FULLSCREEN: bool = False
DEFAULT_RESIZABLE: bool = False

# Audio defaults
DEFAULT_AUDIO_FREQUENCY: int = 44100
DEFAULT_AUDIO_SIZE: int = -16
DEFAULT_AUDIO_CHANNELS: int = 2
DEFAULT_AUDIO_BUFFER: int = 2048
DEFAULT_MASTER_VOLUME: float = 1.0

# Performance defaults
DEFAULT_TARGET_FPS: int = 60
TARGET_FPS: int = 60
DEFAULT_MAX_DELTA_TIME: float = 0.1

# Color constants - 8-bit retro palette
BLACK: Tuple[int, int, int] = (0, 0, 0)
WHITE: Tuple[int, int, int] = (255, 255, 255)
RED: Tuple[int, int, int] = (255, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)
BLUE: Tuple[int, int, int] = (0, 0, 255)
YELLOW: Tuple[int, int, int] = (255, 255, 0)
CYAN: Tuple[int, int, int] = (0, 255, 255)
MAGENTA: Tuple[int, int, int] = (255, 0, 255)
ORANGE: Tuple[int, int, int] = (255, 165, 0)
PURPLE: Tuple[int, int, int] = (128, 0, 128)
GRAY: Tuple[int, int, int] = (128, 128, 128)
DARK_GRAY: Tuple[int, int, int] = (64, 64, 64)
LIGHT_GRAY: Tuple[int, int, int] = (192, 192, 192)

# UI defaults and colors
DEFAULT_BUTTON_COLOR: Tuple[int, int, int] = (100, 100, 100)
BUTTON_COLOR: Tuple[int, int, int] = (100, 100, 100)
DEFAULT_BUTTON_HOVER_COLOR: Tuple[int, int, int] = (150, 150, 150)
BUTTON_HOVER_COLOR: Tuple[int, int, int] = (150, 150, 150)
BUTTON_TEXT_COLOR: Tuple[int, int, int] = WHITE
DEFAULT_BACKGROUND_COLOR: Tuple[int, int, int] = (20, 20, 40)
BACKGROUND_COLOR: Tuple[int, int, int] = (20, 20, 40)

# Game constants
GRID_SIZE: int = 20  # For grid-based games (Snake, Pac-Man)

