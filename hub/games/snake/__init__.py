"""Snake game module."""

# Export new modular version
from hub.games.snake.game import SnakeGameModular

# Import old version from parent directory file for backward compatibility
import importlib.util
import os
_old_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'snake.py')
if os.path.exists(_old_file):
    spec = importlib.util.spec_from_file_location("hub.games.snake_old", _old_file)
    _old_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_old_module)
    SnakeGame = _old_module.SnakeGame
else:
    # Fallback to new version if old doesn't exist
    SnakeGame = SnakeGameModular

__all__ = ['SnakeGameModular', 'SnakeGame']
