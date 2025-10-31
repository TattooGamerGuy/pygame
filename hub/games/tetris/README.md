# Tetris Game - Modular Architecture

Professional modular directory structure for the Tetris game implementation.

## Directory Structure

```
tetris/
├── __init__.py              # Module exports
├── constants.py              # Game constants, shapes, colors
├── README.md                 # Documentation
├── game/                     # Game logic module
│   ├── __init__.py
│   └── game.py              # TetrisGameModular main class
└── components/              # Game entities/components
    ├── __init__.py
    └── tetromino.py         # Tetromino piece component
```

## Module Descriptions

### `constants.py`
Game configuration constants:
- `SHAPES` - Tetromino shape definitions
- `SHAPE_COLORS` - Colors for each shape type
- Grid settings: `GRID_WIDTH`, `GRID_HEIGHT`, `CELL_SIZE`
- Timing: `FALL_INTERVAL`, `FAST_FALL_INTERVAL`
- Scoring: `LINE_CLEAR_BASE_SCORE`

### `game/game.py`
Main game class (`TetrisGameModular`) that:
- Manages game grid state
- Handles piece spawning and rotation
- Processes input (movement, rotation, fast fall)
- Handles line clearing and scoring
- Renders game scene and preview

### `components/tetromino.py`
Tetromino component:
- Shape representation
- Rotation logic
- Position management
- Cell coordinate calculation

## Architecture Principles

1. **Component-Based**: Tetromino is a self-contained component
2. **Separation of Concerns**: Game logic, rendering, and components separated
3. **Dependency Injection**: Game receives services via constructor
4. **Constants Centralization**: All game constants in one place

