# Testing Guide - TDD Approach for Space Invaders

## Overview

This project uses **Test-Driven Development (TDD)** methodology:
1. **RED**: Write failing test first
2. **GREEN**: Write minimum code to pass
3. **REFACTOR**: Improve code while keeping tests green

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Category
```bash
# Unit tests only
pytest tests/space_invaders/test_bullet.py

# Integration tests
pytest tests/space_invaders/test_game_integration.py

# With coverage
pytest --cov=hub/games/space_invaders --cov-report=html
```

### Run Tests Matching Pattern
```bash
pytest -k "bullet"  # Run all bullet-related tests
pytest -k "direction"  # Run direction tests
```

## Test Structure

### Unit Tests
- `test_bullet.py` - Bullet component (direction, movement, boundaries)
- `test_player.py` - Player movement and acceleration
- `test_enemy.py` - Enemy AI and formation
- `test_shields.py` - Shield mechanics
- `test_scoring.py` - Scoring validation

### Integration Tests
- `test_collisions.py` - Collision detection
- `test_waves.py` - Wave progression
- `test_game_integration.py` - Full game mechanics

## Writing New Tests (TDD)

### Step 1: Write Test First
```python
def test_new_feature(self, pygame_init):
    """Test that new feature works correctly."""
    # Arrange
    obj = Component(param1, param2)
    
    # Act
    result = obj.doSomething()
    
    # Assert
    assert result == expected_value
```

### Step 2: Run Test (Should Fail)
```bash
pytest tests/space_invaders/test_component.py::TestComponent::test_new_feature
```

### Step 3: Implement Feature
Write minimum code to make test pass.

### Step 4: Refactor
Improve code while keeping tests green.

## Current Test Coverage

Run `pytest --cov=hub/games/space_invaders` to see coverage report.

**Target**: >80% coverage for game logic components.

## Common Test Patterns

### Testing Movement
```python
def test_movement_direction(self, pygame_init):
    obj = Component(x=100, y=200)
    initial_x = obj.x
    obj.update(dt=0.1, direction=1)
    assert obj.x > initial_x
```

### Testing Collisions
```python
def test_collision_detection(self, pygame_init):
    obj1 = Component(x=100, y=100)
    obj2 = Component(x=105, y=100)
    assert obj1.get_rect().colliderect(obj2.get_rect())
```

### Testing State Changes
```python
def test_state_transition(self, pygame_init):
    game = Game()
    assert game.state == 'initial'
    game.start()
    assert game.state == 'playing'
```

## Fixtures

- `pygame_init` - Initializes pygame for tests
- `mock_surface` - Creates pygame surface for rendering tests
- `mock_services` - Creates mock services for game integration tests

## Continuous Integration

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- See `.github/workflows/tests.yml`

## Debugging Failed Tests

1. Run with verbose output: `pytest -v`
2. Run with print statements: `pytest -s`
3. Run specific test: `pytest tests/path/to/test.py::TestClass::test_method`
4. Use pdb: Add `import pdb; pdb.set_trace()` in test

## Best Practices

1. **Test One Thing**: Each test should verify one behavior
2. **Arrange-Act-Assert**: Clear structure in tests
3. **Descriptive Names**: Test names should describe what they test
4. **Fast Tests**: Unit tests should run quickly (< 1 second each)
5. **Isolated Tests**: Tests should not depend on each other
6. **Test Edge Cases**: Boundary conditions, null values, etc.

