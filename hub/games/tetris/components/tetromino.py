"""Tetromino component for Tetris."""

from typing import List, Tuple
from hub.games.tetris.constants import SHAPES, SHAPE_COLORS


class Tetromino:
    """A Tetris piece component."""
    
    def __init__(self, shape_index: int, x: int, y: int):
        """
        Initialize tetromino.
        
        Args:
            shape_index: Index into SHAPES array
            x: Grid X position
            y: Grid Y position
        """
        self.shape_index = shape_index
        self.shape = [row[:] for row in SHAPES[shape_index]]
        self.color = SHAPE_COLORS[shape_index]
        self.x = x
        self.y = y
    
    def rotate(self) -> List[List[int]]:
        """
        Get rotated shape (90 degrees clockwise).
        
        Returns:
            Rotated shape matrix
        """
        if not self.shape:
            return []
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = self.shape[i][j]
        return rotated
    
    def get_cells(self) -> List[Tuple[int, int]]:
        """
        Get list of (grid_x, grid_y) positions occupied by this piece.
        
        Returns:
            List of (x, y) grid positions
        """
        cells = []
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    cells.append((self.x + j, self.y + i))
        return cells

