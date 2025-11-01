"""
Statistics tracking service.

Tracks player statistics, game statistics, and provides
statistics visualization and export.
"""

from typing import Dict, Optional, Any
import os
import json
import time


class StatisticsService:
    """Service for tracking and managing game statistics."""
    
    def __init__(self):
        """Initialize statistics service."""
        self._statistics: Dict[str, Any] = {}
        self._game_statistics: Dict[str, Dict[str, Any]] = {}
        self._persistence_directory: Optional[str] = None
        self._last_save_time = 0.0
        self._auto_save_interval = 300.0  # 5 minutes
    
    def set_persistence_directory(self, directory: str) -> None:
        """Set persistence directory."""
        self._persistence_directory = directory
        os.makedirs(directory, exist_ok=True)
    
    def track(self, statistic_name: str, value: Any) -> None:
        """
        Track or set a statistic.
        
        Args:
            statistic_name: Name of statistic
            value: Value to set
        """
        self._statistics[statistic_name] = value
        self._check_auto_save()
    
    def increment(self, statistic_name: str, amount: float = 1.0) -> None:
        """
        Increment a statistic.
        
        Args:
            statistic_name: Name of statistic
            amount: Amount to increment by
        """
        current = self._statistics.get(statistic_name, 0)
        self._statistics[statistic_name] = current + amount
        self._check_auto_save()
    
    def update_max(self, statistic_name: str, value: float) -> None:
        """
        Update maximum statistic value.
        
        Args:
            statistic_name: Name of statistic
            value: New value (only updates if greater than current)
        """
        current = self._statistics.get(statistic_name, float('-inf'))
        if value > current:
            self._statistics[statistic_name] = value
            self._check_auto_save()
    
    def get_statistic(self, statistic_name: str, default: Any = 0) -> Any:
        """
        Get statistic value.
        
        Args:
            statistic_name: Name of statistic
            default: Default value if not found
            
        Returns:
            Statistic value
        """
        return self._statistics.get(statistic_name, default)
    
    def get_all_statistics(self) -> Dict[str, Any]:
        """Get all statistics."""
        return self._statistics.copy()
    
    def track_game_stat(self, game_name: str, stat_name: str, value: Any) -> None:
        """
        Track game-specific statistic.
        
        Args:
            game_name: Name of game
            stat_name: Statistic name
            value: Value to set
        """
        if game_name not in self._game_statistics:
            self._game_statistics[game_name] = {}
        self._game_statistics[game_name][stat_name] = value
        self._check_auto_save()
    
    def get_game_statistics(self, game_name: str) -> Dict[str, Any]:
        """
        Get all statistics for a game.
        
        Args:
            game_name: Name of game
            
        Returns:
            Dictionary of game statistics
        """
        return self._game_statistics.get(game_name, {}).copy()
    
    def save(self) -> bool:
        """
        Save statistics to disk.
        
        Returns:
            True if successful
        """
        if not self._persistence_directory:
            return False
        
        try:
            path = os.path.join(self._persistence_directory, "statistics.json")
            data = {
                'statistics': self._statistics,
                'game_statistics': self._game_statistics,
                'timestamp': time.time()
            }
            with open(path, 'w') as f:
                json.dump(data, f)
            self._last_save_time = time.time()
            return True
        except Exception:
            return False
    
    def load(self) -> bool:
        """
        Load statistics from disk.
        
        Returns:
            True if successful
        """
        if not self._persistence_directory:
            return False
        
        try:
            path = os.path.join(self._persistence_directory, "statistics.json")
            if not os.path.exists(path):
                return False
            
            with open(path, 'r') as f:
                data = json.load(f)
            
            self._statistics = data.get('statistics', {})
            self._game_statistics = data.get('game_statistics', {})
            return True
        except Exception:
            return False
    
    def export(self, filepath: str) -> bool:
        """
        Export statistics to file.
        
        Args:
            filepath: Path to export file
            
        Returns:
            True if successful
        """
        try:
            data = {
                'statistics': self._statistics,
                'game_statistics': self._game_statistics,
                'export_timestamp': time.time()
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def reset(self) -> None:
        """Reset all statistics."""
        self._statistics.clear()
        self._game_statistics.clear()
    
    def _check_auto_save(self) -> None:
        """Check if auto-save is needed."""
        if self._persistence_directory:
            current_time = time.time()
            if current_time - self._last_save_time >= self._auto_save_interval:
                self.save()

