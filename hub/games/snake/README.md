# Snake Game - Modular Architecture

Professional modular directory structure for the Snake game implementation.

## Directory Structure

```
snake/
├── __init__.py              # Module exports
├── constants.py             # Game constants and configuration
├── README.md                 # Documentation
├── game/                     # Game logic module
│   ├── __init__.py
│   └── game.py              # SnakeGameModular main class
└── components/              # (Reserved for future components)
    └── __init__.py
```

## Module Descriptions

### `constants.py`
Game configuration constants:
- `INITIAL_MOVE_INTERVAL` - Initial snake movement speed
- `MIN_MOVE_INTERVAL` - Maximum speed limit
- `SPEED_INCREASE_FACTOR` - Speed increase per food eaten
- `FOOD_SCORE` - Points per food

### `game/game.py`
Main game class (`SnakeGameModular`) that:
- Manages snake state (list of grid positions)
- Handles input for direction changes
- Updates snake movement
- Spawns and tracks food
- Handles collision detection
- Renders game scene

## Architecture Principles

1. **Simple Structure**: Snake is represented as a list of tuples (grid positions)
2. **Dependency Injection**: Game receives services via constructor
3. **Modularity**: Game logic separated from rendering
4. **Extensibility**: Components directory reserved for future enhancements

