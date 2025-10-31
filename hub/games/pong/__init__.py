"""Pong game module."""

# Export new modular version
from hub.games.pong.game import PongGameModular

# Import old version from parent directory file for backward compatibility
import importlib.util
import os
_old_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pong.py')
if os.path.exists(_old_file):
    spec = importlib.util.spec_from_file_location("hub.games.pong_old", _old_file)
    _old_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_old_module)
    PongGame = _old_module.PongGame
else:
    # Fallback to new version if old doesn't exist
    PongGame = PongGameModular

__all__ = ['PongGameModular', 'PongGame']
