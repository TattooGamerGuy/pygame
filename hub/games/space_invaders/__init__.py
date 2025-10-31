"""Space Invaders game module."""

# Export new modular version
from hub.games.space_invaders.game import SpaceInvadersGameModular

# Import old version from parent directory file for backward compatibility
import importlib.util
import os
_old_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'space_invaders.py')
if os.path.exists(_old_file):
    spec = importlib.util.spec_from_file_location("hub.games.space_invaders_old", _old_file)
    _old_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_old_module)
    SpaceInvadersGame = _old_module.SpaceInvadersGame
else:
    # Fallback to new version if old doesn't exist
    SpaceInvadersGame = SpaceInvadersGameModular

__all__ = ['SpaceInvadersGameModular', 'SpaceInvadersGame']
