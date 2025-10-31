"""AI controller for paddle."""

from typing import Optional
from hub.games.pong.components.paddle import Paddle


class PaddleAI:
    """AI controller for paddle movement."""
    
    def __init__(self, paddle: Paddle):
        """
        Initialize AI controller.
        
        Args:
            paddle: Paddle to control
        """
        self.paddle = paddle
        self.follow_threshold = 10  # pixels threshold for following
    
    def get_direction(self, ball_y: Optional[float]) -> int:
        """
        Get direction for AI paddle to move.
        
        Args:
            ball_y: Y position of ball
            
        Returns:
            -1 for up, 1 for down, 0 for no movement
        """
        if ball_y is None:
            return 0
        
        paddle_center = self.paddle.get_center_y()
        
        # Simple AI: follow ball
        if paddle_center < ball_y - self.follow_threshold:
            return 1  # Move down
        elif paddle_center > ball_y + self.follow_threshold:
            return -1  # Move up
        else:
            return 0  # Stay in place

