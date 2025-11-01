"""
Achievement system service.

Manages achievements, progress tracking, and unlock notifications.
"""

from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from dataclasses import dataclass, field
import os
import json
import time


class AchievementStatus(Enum):
    """Achievement status."""
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    HIDDEN = "hidden"


@dataclass
class Achievement:
    """Achievement definition."""
    id: str
    name: str
    description: str
    condition: Callable[[Dict[str, Any]], bool]
    game: Optional[str] = None
    progress_callback: Optional[Callable[[Dict[str, Any]], float]] = None
    icon: Optional[str] = None
    points: int = 0
    hidden: bool = False
    unlock_time: Optional[float] = None
    
    def check(self, statistics: Dict[str, Any]) -> bool:
        """
        Check if achievement should be unlocked.
        
        Args:
            statistics: Current statistics
            
        Returns:
            True if unlocked
        """
        try:
            return self.condition(statistics)
        except Exception:
            return False
    
    def get_progress(self, statistics: Dict[str, Any]) -> float:
        """
        Get achievement progress (0.0 to 1.0).
        
        Args:
            statistics: Current statistics
            
        Returns:
            Progress value
        """
        if self.progress_callback:
            try:
                return max(0.0, min(1.0, self.progress_callback(statistics)))
            except Exception:
                return 0.0
        return 1.0 if self.check(statistics) else 0.0


class AchievementService:
    """Service for managing achievements."""
    
    def __init__(self):
        """Initialize achievement service."""
        self._achievements: Dict[str, Achievement] = {}
        self._unlocked_achievements: Dict[str, float] = {}  # achievement_id -> unlock_time
        self._persistence_directory: Optional[str] = None
        self.on_achievement_unlocked: Optional[Callable[[str], None]] = None
    
    def set_persistence_directory(self, directory: str) -> None:
        """Set persistence directory."""
        self._persistence_directory = directory
        os.makedirs(directory, exist_ok=True)
    
    def register(self, achievement: Achievement) -> None:
        """
        Register an achievement.
        
        Args:
            achievement: Achievement to register
        """
        self._achievements[achievement.id] = achievement
    
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """Get achievement by ID."""
        return self._achievements.get(achievement_id)
    
    def check_achievements(self, statistics: Dict[str, Any]) -> List[str]:
        """
        Check all achievements against statistics.
        
        Args:
            statistics: Current statistics
            
        Returns:
            List of newly unlocked achievement IDs
        """
        newly_unlocked = []
        
        for achievement_id, achievement in self._achievements.items():
            if achievement_id in self._unlocked_achievements:
                continue  # Already unlocked
            
            if achievement.check(statistics):
                self._unlocked_achievements[achievement_id] = time.time()
                achievement.unlock_time = time.time()
                newly_unlocked.append(achievement_id)
                
                if self.on_achievement_unlocked:
                    self.on_achievement_unlocked(achievement_id)
        
        return newly_unlocked
    
    def get_achievement_status(self, achievement_id: str) -> AchievementStatus:
        """
        Get achievement status.
        
        Args:
            achievement_id: Achievement ID
            
        Returns:
            Achievement status
        """
        if achievement_id not in self._achievements:
            return AchievementStatus.LOCKED
        
        if achievement_id in self._unlocked_achievements:
            return AchievementStatus.UNLOCKED
        
        achievement = self._achievements[achievement_id]
        if achievement.hidden:
            return AchievementStatus.HIDDEN
        
        return AchievementStatus.LOCKED
    
    def get_achievement_progress(
        self,
        achievement_id: str,
        statistics: Dict[str, Any]
    ) -> float:
        """
        Get achievement progress.
        
        Args:
            achievement_id: Achievement ID
            statistics: Current statistics
            
        Returns:
            Progress (0.0 to 1.0)
        """
        achievement = self._achievements.get(achievement_id)
        if not achievement:
            return 0.0
        
        if achievement_id in self._unlocked_achievements:
            return 1.0
        
        return achievement.get_progress(statistics)
    
    def get_game_achievements(self, game_name: str) -> List[Achievement]:
        """
        Get all achievements for a game.
        
        Args:
            game_name: Name of game
            
        Returns:
            List of achievements
        """
        return [
            achievement
            for achievement in self._achievements.values()
            if achievement.game == game_name
        ]
    
    def get_unlocked_achievements(self) -> List[str]:
        """Get list of unlocked achievement IDs."""
        return list(self._unlocked_achievements.keys())
    
    def save(self) -> bool:
        """Save achievement data."""
        if not self._persistence_directory:
            return False
        
        try:
            path = os.path.join(self._persistence_directory, "achievements.json")
            data = {
                'unlocked': self._unlocked_achievements,
                'timestamp': time.time()
            }
            with open(path, 'w') as f:
                json.dump(data, f)
            return True
        except Exception:
            return False
    
    def load(self) -> bool:
        """Load achievement data."""
        if not self._persistence_directory:
            return False
        
        try:
            path = os.path.join(self._persistence_directory, "achievements.json")
            if not os.path.exists(path):
                return False
            
            with open(path, 'r') as f:
                data = json.load(f)
            
            self._unlocked_achievements = data.get('unlocked', {})
            
            # Update achievement unlock times
            for achievement_id, unlock_time in self._unlocked_achievements.items():
                if achievement_id in self._achievements:
                    self._achievements[achievement_id].unlock_time = unlock_time
            
            return True
        except Exception:
            return False

