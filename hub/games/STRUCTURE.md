# Games Directory Structure

All games have been refactored into professional modular directory structures following consistent patterns.

## Standard Structure

Each game follows this structure:

```
game_name/
├── __init__.py              # Module exports (exports GameModular class)
├── constants.py              # Game-specific constants and configuration
├── README.md                 # Game-specific documentation
├── game/                     # Game logic module
│   ├── __init__.py
│   └── game.py              # Main game class (GameModular)
├── components/              # Game entities/components
│   ├── __init__.py
│   └── [component files]   # Component classes
└── [additional modules]     # Game-specific modules (ai/, maze.py, etc.)
```

## Game Directories

### 1. Pong (`hub/games/pong/`)
```
pong/
├── __init__.py
├── constants.py
├── README.md
├── game/
│   ├── __init__.py
│   └── game.py              # PongGameModular
├── components/
│   ├── __init__.py
│   ├── paddle.py
│   └── ball.py
└── ai/
    ├── __init__.py
    └── paddle_ai.py         # AI controller
```

### 2. Snake (`hub/games/snake/`)
```
snake/
├── __init__.py
├── constants.py
├── README.md
├── game/
│   ├── __init__.py
│   └── game.py              # SnakeGameModular
└── components/
    └── __init__.py          # (Simple game, no separate components)
```

### 3. Space Invaders (`hub/games/space_invaders/`)
```
space_invaders/
├── __init__.py
├── constants.py
├── README.md
├── game/
│   ├── __init__.py
│   └── game.py              # SpaceInvadersGameModular
└── components/
    ├── __init__.py
    ├── bullet.py
    ├── enemy.py
    └── player.py
```

### 4. Tetris (`hub/games/tetris/`)
```
tetris/
├── __init__.py
├── constants.py              # Includes shapes and colors
├── README.md
├── game/
│   ├── __init__.py
│   └── game.py              # TetrisGameModular
└── components/
    ├── __init__.py
    └── tetromino.py
```

### 5. Pac-Man (`hub/games/pacman/`)
```
pacman/
├── __init__.py
├── constants.py
├── maze.py                   # Maze layout definition
├── README.md
├── game/
│   ├── __init__.py
│   └── game.py              # PacManGameModular
└── components/
    ├── __init__.py
    ├── player.py
    └── ghost.py
```

## Principles

1. **Separation of Concerns**: Game logic, components, constants separated
2. **Modularity**: Each component is self-contained
3. **Dependency Injection**: All games use DI pattern via BaseGameModular
4. **Consistency**: All games follow the same structure pattern
5. **Documentation**: Each game has its own README.md
6. **Extensibility**: Easy to add new components or modules

## Usage

Import games using:
```python
from hub.games.pong import PongGameModular
from hub.games.snake import SnakeGameModular
from hub.games.space_invaders import SpaceInvadersGameModular
from hub.games.tetris import TetrisGameModular
from hub.games.pacman import PacManGameModular
```

## Benefits

- **Professional Structure**: Industry-standard organization
- **Easy Navigation**: Clear separation makes code easy to find
- **Maintainability**: Changes are isolated to specific modules
- **Testability**: Components can be tested independently
- **Scalability**: Easy to add new features without breaking existing code

