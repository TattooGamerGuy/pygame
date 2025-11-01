"""
Leaderboard service.

Manages leaderboards, score submission, and rankings.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
import os
import json
import time


class LeaderboardType(Enum):
    """Leaderboard type."""
    HIGH_SCORE = "high_score"  # Highest scores first
    LOW_SCORE = "low_score"  # Lowest scores first
    TIME_ATTACK = "time_attack"  # Fastest times first
    ACCURACY = "accuracy"  # Highest accuracy first


@dataclass
class LeaderboardEntry:
    """Leaderboard entry."""
    player_name: str
    score: float
    timestamp: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize metadata."""
        if self.metadata is None:
            self.metadata = {}


class LeaderboardService:
    """Service for managing leaderboards."""
    
    def __init__(self):
        """Initialize leaderboard service."""
        self._leaderboards: Dict[str, LeaderboardType] = {}
        self._entries: Dict[str, List[LeaderboardEntry]] = {}
        self._persistence_directory: Optional[str] = None
    
    def set_persistence_directory(self, directory: str) -> None:
        """Set persistence directory."""
        self._persistence_directory = directory
        os.makedirs(directory, exist_ok=True)
    
    def create_leaderboard(
        self,
        leaderboard_id: str,
        board_type: LeaderboardType
    ) -> None:
        """
        Create a new leaderboard.
        
        Args:
            leaderboard_id: Leaderboard identifier
            board_type: Type of leaderboard
        """
        self._leaderboards[leaderboard_id] = board_type
        if leaderboard_id not in self._entries:
            self._entries[leaderboard_id] = []
    
    def leaderboard_exists(self, leaderboard_id: str) -> bool:
        """Check if leaderboard exists."""
        return leaderboard_id in self._leaderboards
    
    def submit_score(
        self,
        leaderboard_id: str,
        player_name: str,
        score: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[LeaderboardEntry]:
        """
        Submit a score to leaderboard.
        
        Args:
            leaderboard_id: Leaderboard identifier
            player_name: Player name
            score: Score value
            metadata: Optional metadata
            
        Returns:
            Created entry or None if failed
        """
        if leaderboard_id not in self._leaderboards:
            return None
        
        entry = LeaderboardEntry(
            player_name=player_name,
            score=score,
            timestamp=time.time(),
            metadata=metadata or {}
        )
        
        self._entries[leaderboard_id].append(entry)
        self._sort_leaderboard(leaderboard_id)
        
        return entry
    
    def get_leaderboard(
        self,
        leaderboard_id: str,
        limit: Optional[int] = None
    ) -> List[LeaderboardEntry]:
        """
        Get leaderboard entries.
        
        Args:
            leaderboard_id: Leaderboard identifier
            limit: Maximum number of entries to return
            
        Returns:
            List of entries (sorted)
        """
        if leaderboard_id not in self._entries:
            return []
        
        entries = self._entries[leaderboard_id].copy()
        
        if limit:
            entries = entries[:limit]
        
        return entries
    
    def get_player_ranking(
        self,
        leaderboard_id: str,
        player_name: str
    ) -> Optional[int]:
        """
        Get player's ranking.
        
        Args:
            leaderboard_id: Leaderboard identifier
            player_name: Player name
            
        Returns:
            Ranking (1-based) or None if not found
        """
        if leaderboard_id not in self._entries:
            return None
        
        entries = self._entries[leaderboard_id]
        
        for i, entry in enumerate(entries):
            if entry.player_name == player_name:
                return i + 1  # 1-based ranking
        
        return None
    
    def _sort_leaderboard(self, leaderboard_id: str) -> None:
        """Sort leaderboard based on type."""
        if leaderboard_id not in self._leaderboards:
            return
        
        board_type = self._leaderboards[leaderboard_id]
        entries = self._entries[leaderboard_id]
        
        if board_type == LeaderboardType.HIGH_SCORE:
            entries.sort(key=lambda e: e.score, reverse=True)
        elif board_type == LeaderboardType.LOW_SCORE:
            entries.sort(key=lambda e: e.score, reverse=False)
        elif board_type == LeaderboardType.TIME_ATTACK:
            entries.sort(key=lambda e: e.score, reverse=False)  # Lower time is better
        elif board_type == LeaderboardType.ACCURACY:
            entries.sort(key=lambda e: e.score, reverse=True)  # Higher accuracy is better
    
    def save(self) -> bool:
        """Save leaderboards to disk."""
        if not self._persistence_directory:
            return False
        
        try:
            path = os.path.join(self._persistence_directory, "leaderboards.json")
            data = {
                'leaderboards': {
                    k: v.value for k, v in self._leaderboards.items()
                },
                'entries': {
                    k: [
                        {
                            'player_name': e.player_name,
                            'score': e.score,
                            'timestamp': e.timestamp,
                            'metadata': e.metadata
                        }
                        for e in entries
                    ]
                    for k, entries in self._entries.items()
                }
            }
            with open(path, 'w') as f:
                json.dump(data, f)
            return True
        except Exception:
            return False
    
    def load(self) -> bool:
        """Load leaderboards from disk."""
        if not self._persistence_directory:
            return False
        
        try:
            path = os.path.join(self._persistence_directory, "leaderboards.json")
            if not os.path.exists(path):
                return False
            
            with open(path, 'r') as f:
                data = json.load(f)
            
            # Load leaderboard types
            for k, v in data.get('leaderboards', {}).items():
                self._leaderboards[k] = LeaderboardType(v)
            
            # Load entries
            for k, entries_data in data.get('entries', {}).items():
                self._entries[k] = [
                    LeaderboardEntry(
                        player_name=e['player_name'],
                        score=e['score'],
                        timestamp=e['timestamp'],
                        metadata=e.get('metadata', {})
                    )
                    for e in entries_data
                ]
                self._sort_leaderboard(k)
            
            return True
        except Exception:
            return False

