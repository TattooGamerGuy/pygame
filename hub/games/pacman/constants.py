"""Constants for Pac-Man game."""

from hub.config.defaults import SCREEN_WIDTH, SCREEN_HEIGHT

# Maze dimensions
MAZE_WIDTH = 28
MAZE_HEIGHT = 30
CELL_SIZE = min(SCREEN_WIDTH // MAZE_WIDTH, (SCREEN_HEIGHT - 100) // MAZE_HEIGHT)
MAZE_X = (SCREEN_WIDTH - MAZE_WIDTH * CELL_SIZE) // 2
MAZE_Y = 50

# Scoring
DOT_SCORE = 10
POWER_PELLET_SCORE = 50
GHOST_SCORE = 200
CLEAR_BONUS = 1000

# Player settings
PLAYER_SPEED = 2  # pixels per frame
POWER_MODE_DURATION = 10.0  # seconds

# Ghost settings
GHOST_SPEED = 1.5

