# Pac-Man Game - Modular Architecture

Professional modular directory structure for the Pac-Man game implementation.

## Directory Structure

```
pacman/
├── __init__.py              # Module exports
├── constants.py              # Game constants and configuration
├── maze.py                   # Maze layout definition
├── README.md                 # Documentation
├── game/                     # Game logic module
│   ├── __init__.py
│   └── game.py              # PacManGameModular main class
└── components/              # Game entities/components
    ├── __init__.py
    ├── player.py            # Player component
    └── ghost.py             # Ghost enemy component
```

## Module Descriptions

### `constants.py`
Game configuration constants:
- Maze dimensions and cell size
- Scoring: `DOT_SCORE`, `POWER_PELLET_SCORE`, `GHOST_SCORE`, `CLEAR_BONUS`
- Player settings: `PLAYER_SPEED`, `POWER_MODE_DURATION`
- Ghost settings: `GHOST_SPEED`

### `maze.py`
Maze layout definition:
- `MAZE_LAYOUT` - 2D array representing maze (1=wall, 0=path, 2=dot, 3=power pellet)

### `game/game.py`
Main game class (`PacManGameModular`) that:
- Manages game state and maze
- Handles input for player movement
- Updates player and ghosts
- Handles dot collection and scoring
- Manages power mode
- Handles collision detection
- Renders game scene

### `components/`
Game entities/components:
- **player.py**: Player component with movement, power mode, and maze navigation
- **ghost.py**: Ghost component with AI and collision detection

## Architecture Principles

1. **Component-Based**: Player and Ghost are self-contained components
2. **Separation of Concerns**: Game logic, components, and maze layout separated
3. **Dependency Injection**: Game receives services via constructor
4. **Data Separation**: Maze layout in separate file for easy modification

