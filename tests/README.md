# Space Invaders Test Suite

## Overview

Comprehensive test suite for Space Invaders game using Test-Driven Development (TDD) approach.

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Module
```bash
pytest tests/space_invaders/test_bullet.py
```

### Run with Coverage
```bash
pytest --cov=hub/games/space_invaders
```

### Run with Verbose Output
```bash
pytest -v
```

## Test Structure

### Unit Tests
- `test_bullet.py` - Bullet component tests (direction, movement, boundaries)
- `test_player.py` - Player movement and acceleration tests
- `test_enemy.py` - Enemy AI and formation tests
- `test_shields.py` - Shield mechanics and damage tests

### Integration Tests
- `test_collisions.py` - Collision detection between game objects
- `test_waves.py` - Wave progression and difficulty scaling
- `test_scoring.py` - Scoring system validation

## TDD Approach

1. **Write Tests First** - Define expected behavior in tests before implementation
2. **Red Phase** - Tests should fail initially
3. **Green Phase** - Implement minimum code to pass tests
4. **Refactor** - Improve code while keeping tests passing

## Test Coverage Goals

- Aim for >80% code coverage
- All critical game mechanics should have tests
- Edge cases and boundary conditions covered

## Future Test Categories

- Game state management
- Audio system
- Visual effects (particles, screen shake)
- Input handling
- High score persistence
- Menu navigation

