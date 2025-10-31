"""Constants for Tetris game."""

from hub.config.defaults import CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE

# Tetromino shapes (1 = filled, 0 = empty)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

# Grid settings
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Timing
FALL_INTERVAL = 0.5
FAST_FALL_INTERVAL = 0.05

# Scoring
LINE_CLEAR_BASE_SCORE = 100
