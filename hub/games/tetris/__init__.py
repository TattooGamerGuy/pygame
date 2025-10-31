"""Tetris game module."""

# Export new modular version
from hub.games.tetris.game import TetrisGameModular

# Import old version from parent directory file for backward compatibility
import importlib.util
import os
_old_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tetris.py')
if os.path.exists(_old_file):
    spec = importlib.util.spec_from_file_location("hub.games.tetris_old", _old_file)
    _old_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_old_module)
    TetrisGame = _old_module.TetrisGame
else:
    # Fallback to new version if old doesn't exist
    TetrisGame = TetrisGameModular

__all__ = ['TetrisGameModular', 'TetrisGame']
