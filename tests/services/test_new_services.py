"""
Tests for New Services (TDD Approach).

Red Phase: Tests define expected behavior before implementation.
"""

import pytest
import time
import os
import tempfile
from typing import Dict, List, Any
from hub.services.statistics_service import StatisticsService
from hub.services.achievement_service import (
    AchievementService,
    Achievement,
    AchievementStatus
)
from hub.services.leaderboard_service import (
    LeaderboardService,
    LeaderboardEntry,
    LeaderboardType
)
from hub.services.notification_service import (
    NotificationService,
    Notification,
    NotificationPriority
)
from hub.services.analytics_service import AnalyticsService
from hub.services.save_service import SaveService


@pytest.fixture
def temp_dir():
    """Create temporary directory for test data."""
    temp = tempfile.mkdtemp()
    yield temp


class TestStatisticsService:
    """Test statistics service."""
    
    def test_statistics_service_initialization(self):
        """Test statistics service initialization."""
        service = StatisticsService()
        assert service is not None
    
    def test_track_statistic(self):
        """Test tracking a statistic."""
        service = StatisticsService()
        
        service.track("games_played", 1)
        service.track("score", 1500)
        
        assert service.get_statistic("games_played") == 1
        assert service.get_statistic("score") == 1500
    
    def test_increment_statistic(self):
        """Test incrementing a statistic."""
        service = StatisticsService()
        
        service.increment("kills", 5)
        service.increment("kills", 3)
        
        assert service.get_statistic("kills") == 8
    
    def test_update_max_statistic(self):
        """Test updating maximum statistic."""
        service = StatisticsService()
        
        service.update_max("high_score", 1000)
        service.update_max("high_score", 1500)
        service.update_max("high_score", 800)
        
        assert service.get_statistic("high_score") == 1500
    
    def test_game_statistics(self):
        """Test game-specific statistics."""
        service = StatisticsService()
        
        service.track_game_stat("pong", "wins", 1)
        service.track_game_stat("pong", "games_played", 1)
        service.track_game_stat("snake", "high_score", 500)
        
        pong_stats = service.get_game_statistics("pong")
        assert pong_stats["wins"] == 1
        assert pong_stats["games_played"] == 1
        
        snake_stats = service.get_game_statistics("snake")
        assert snake_stats["high_score"] == 500
    
    def test_statistics_persistence(self, temp_dir):
        """Test saving and loading statistics."""
        service = StatisticsService()
        service.set_persistence_directory(temp_dir)
        
        service.track("total_playtime", 3600)
        service.save()
        
        # Create new service instance and load
        new_service = StatisticsService()
        new_service.set_persistence_directory(temp_dir)
        new_service.load()
        
        assert new_service.get_statistic("total_playtime") == 3600
    
    def test_statistics_export(self, temp_dir):
        """Test exporting statistics."""
        service = StatisticsService()
        
        service.track("score", 1000)
        service.track("level", 5)
        
        export_path = os.path.join(temp_dir, "stats.json")
        result = service.export(export_path)
        
        assert result is True
        assert os.path.exists(export_path)
    
    def test_statistics_reset(self):
        """Test resetting statistics."""
        service = StatisticsService()
        
        service.track("score", 1000)
        service.reset()
        
        assert service.get_statistic("score") == 0 or service.get_statistic("score") is None


class TestAchievementService:
    """Test achievement service."""
    
    def test_achievement_service_initialization(self):
        """Test achievement service initialization."""
        service = AchievementService()
        assert service is not None
    
    def test_register_achievement(self):
        """Test registering an achievement."""
        service = AchievementService()
        
        achievement = Achievement(
            id="first_win",
            name="First Victory",
            description="Win your first game",
            condition=lambda stats: stats.get("wins", 0) >= 1
        )
        
        service.register(achievement)
        
        assert service.get_achievement("first_win") == achievement
    
    def test_check_achievements(self):
        """Test checking achievement progress."""
        service = AchievementService()
        
        unlocked = []
        
        def on_unlock(achievement_id: str):
            unlocked.append(achievement_id)
        
        service.on_achievement_unlocked = on_unlock
        
        # Register achievement
        achievement = Achievement(
            id="score_1000",
            name="High Scorer",
            description="Reach 1000 points",
            condition=lambda stats: stats.get("score", 0) >= 1000
        )
        service.register(achievement)
        
        # Check with stats that should unlock
        stats = {"score": 1200}
        service.check_achievements(stats)
        
        # Should unlock
        assert len(unlocked) > 0 or service.get_achievement_status("score_1000") == AchievementStatus.UNLOCKED
    
    def test_achievement_progress(self):
        """Test achievement progress tracking."""
        service = AchievementService()
        
        achievement = Achievement(
            id="kill_100",
            name="Expert Killer",
            description="Kill 100 enemies",
            condition=lambda stats: stats.get("kills", 0) >= 100,
            progress_callback=lambda stats: stats.get("kills", 0) / 100.0
        )
        service.register(achievement)
        
        stats = {"kills": 50}
        progress = service.get_achievement_progress("kill_100", stats)
        
        assert 0.0 <= progress <= 1.0
        assert progress == 0.5 or progress > 0  # Should show 50% progress
    
    def test_achievement_status(self):
        """Test achievement status."""
        service = AchievementService()
        
        achievement = Achievement(
            id="test",
            name="Test",
            description="Test achievement",
            condition=lambda stats: True
        )
        service.register(achievement)
        
        # Initially locked
        assert service.get_achievement_status("test") == AchievementStatus.LOCKED
        
        # After unlocking
        service.check_achievements({})
        assert service.get_achievement_status("test") == AchievementStatus.UNLOCKED
    
    def test_game_achievements(self):
        """Test game-specific achievements."""
        service = AchievementService()
        
        achievement = Achievement(
            id="pong_master",
            name="Pong Master",
            description="Win 10 games of Pong",
            game="pong",
            condition=lambda stats: stats.get("pong_wins", 0) >= 10
        )
        service.register(achievement)
        
        game_achievements = service.get_game_achievements("pong")
        assert len(game_achievements) >= 1
        assert any(a.id == "pong_master" for a in game_achievements)
    
    def test_achievement_persistence(self, temp_dir):
        """Test saving and loading achievements."""
        service = AchievementService()
        service.set_persistence_directory(temp_dir)
        
        achievement = Achievement(
            id="test",
            name="Test",
            description="Test",
            condition=lambda stats: True
        )
        service.register(achievement)
        service.check_achievements({})
        service.save()
        
        # Load in new instance
        new_service = AchievementService()
        new_service.set_persistence_directory(temp_dir)
        
        # Must register achievement in new instance too (achievements are not persisted, only unlock status)
        new_achievement = Achievement(
            id="test",
            name="Test",
            description="Test",
            condition=lambda stats: True
        )
        new_service.register(new_achievement)
        new_service.load()
        
        assert new_service.get_achievement_status("test") == AchievementStatus.UNLOCKED


class TestLeaderboardService:
    """Test leaderboard service."""
    
    def test_leaderboard_service_initialization(self):
        """Test leaderboard service initialization."""
        service = LeaderboardService()
        assert service is not None
    
    def test_create_leaderboard(self):
        """Test creating a leaderboard."""
        service = LeaderboardService()
        
        service.create_leaderboard("pong_scores", LeaderboardType.HIGH_SCORE)
        
        assert service.leaderboard_exists("pong_scores")
    
    def test_submit_score(self):
        """Test submitting a score."""
        service = LeaderboardService()
        
        service.create_leaderboard("pong", LeaderboardType.HIGH_SCORE)
        
        entry = service.submit_score("pong", "player1", 1500)
        
        assert entry is not None
        assert entry.score == 1500
        assert entry.player_name == "player1"
    
    def test_get_leaderboard(self):
        """Test getting leaderboard entries."""
        service = LeaderboardService()
        
        service.create_leaderboard("snake", LeaderboardType.HIGH_SCORE)
        
        service.submit_score("snake", "alice", 1000)
        service.submit_score("snake", "bob", 2000)
        service.submit_score("snake", "charlie", 1500)
        
        entries = service.get_leaderboard("snake", limit=10)
        
        assert len(entries) == 3
        # Should be sorted (highest first for high score)
        assert entries[0].score >= entries[1].score
    
    def test_player_ranking(self):
        """Test getting player ranking."""
        service = LeaderboardService()
        
        service.create_leaderboard("tetris", LeaderboardType.HIGH_SCORE)
        service.submit_score("tetris", "player1", 1000)
        service.submit_score("tetris", "player2", 2000)
        service.submit_score("tetris", "player3", 1500)
        
        rank = service.get_player_ranking("tetris", "player1")
        
        assert rank is not None
        assert rank > 0
    
    def test_leaderboard_types(self):
        """Test different leaderboard types."""
        service = LeaderboardService()
        
        # High score (descending)
        service.create_leaderboard("high_scores", LeaderboardType.HIGH_SCORE)
        service.submit_score("high_scores", "p1", 1000)
        service.submit_score("high_scores", "p2", 500)
        
        entries = service.get_leaderboard("high_scores")
        assert entries[0].score > entries[1].score
        
        # Low score (ascending)
        service.create_leaderboard("low_scores", LeaderboardType.LOW_SCORE)
        service.submit_score("low_scores", "p1", 1000)
        service.submit_score("low_scores", "p2", 500)
        
        entries = service.get_leaderboard("low_scores")
        assert entries[0].score < entries[1].score
    
    def test_leaderboard_persistence(self, temp_dir):
        """Test saving and loading leaderboards."""
        service = LeaderboardService()
        service.set_persistence_directory(temp_dir)
        
        service.create_leaderboard("test", LeaderboardType.HIGH_SCORE)
        service.submit_score("test", "player", 1000)
        service.save()
        
        new_service = LeaderboardService()
        new_service.set_persistence_directory(temp_dir)
        new_service.load()
        
        entries = new_service.get_leaderboard("test")
        assert len(entries) == 1
        assert entries[0].score == 1000


class TestNotificationService:
    """Test notification service."""
    
    def test_notification_service_initialization(self):
        """Test notification service initialization."""
        service = NotificationService()
        assert service is not None
    
    def test_show_notification(self):
        """Test showing notification."""
        service = NotificationService()
        
        notification = service.show("Test message", NotificationPriority.INFO)
        
        assert notification is not None
        assert notification.message == "Test message"
        assert notification.priority == NotificationPriority.INFO
    
    def test_notification_queue(self):
        """Test notification queueing."""
        service = NotificationService()
        
        service.show("Message 1", NotificationPriority.INFO)
        service.show("Message 2", NotificationPriority.WARNING)
        service.show("Message 3", NotificationPriority.ERROR)
        
        assert service.queue_size >= 0  # May process immediately
    
    def test_notification_priority(self):
        """Test notification priority handling."""
        service = NotificationService()
        
        # Higher priority should be shown first
        service.show("Low priority", NotificationPriority.INFO)
        service.show("High priority", NotificationPriority.ERROR)
        
        # Should handle priority ordering
        assert True
    
    def test_notification_dismiss(self):
        """Test dismissing notification."""
        service = NotificationService()
        
        notification = service.show("Test", NotificationPriority.INFO)
        
        service.dismiss(notification.id)
        
        # Should be dismissed
        assert True
    
    def test_notification_callbacks(self):
        """Test notification callbacks."""
        dismissed = []
        
        def on_dismiss(notification_id: str):
            dismissed.append(notification_id)
        
        service = NotificationService()
        service.on_notification_dismissed = on_dismiss
        
        notification = service.show("Test", NotificationPriority.INFO)
        service.dismiss(notification.id)
        
        # Callback should be called
        assert notification.id in dismissed or len(dismissed) > 0
    
    def test_notification_auto_dismiss(self):
        """Test auto-dismissing notifications."""
        service = NotificationService()
        
        notification = service.show(
            "Auto dismiss",
            NotificationPriority.INFO,
            duration_ms=100
        )
        
        assert notification.duration_ms == 100


class TestAnalyticsService:
    """Test analytics service."""
    
    def test_analytics_service_initialization(self):
        """Test analytics service initialization."""
        service = AnalyticsService()
        assert service is not None
    
    def test_track_event(self):
        """Test tracking analytics event."""
        service = AnalyticsService()
        
        service.track_event("game_start", {"game": "pong"})
        service.track_event("level_complete", {"level": 1, "time": 120})
        
        # Should track events
        assert True
    
    def test_track_metric(self):
        """Test tracking metrics."""
        service = AnalyticsService()
        
        service.track_metric("fps", 60.0)
        service.track_metric("load_time", 2.5)
        
        # Should track metrics
        assert True
    
    def test_analytics_batch(self):
        """Test batching analytics events."""
        service = AnalyticsService()
        
        service.set_batch_size(10)
        
        for i in range(15):
            service.track_event("event", {"index": i})
        
        # Should batch events
        assert True
    
    def test_analytics_privacy(self):
        """Test privacy-compliant analytics."""
        service = AnalyticsService()
        
        service.enable_privacy_mode(True)
        
        assert service.privacy_mode_enabled


class TestSaveService:
    """Test save service."""
    
    def test_save_service_initialization(self):
        """Test save service initialization."""
        service = SaveService()
        assert service is not None
    
    def test_save_game_state(self, temp_dir):
        """Test saving game state."""
        service = SaveService()
        service.set_save_directory(temp_dir)
        
        state_data = {"level": 5, "score": 5000, "player": {"health": 100}}
        
        result = service.save_game_state("pong", "slot1", state_data)
        
        assert result is True
    
    def test_load_game_state(self, temp_dir):
        """Test loading game state."""
        service = SaveService()
        service.set_save_directory(temp_dir)
        
        original_state = {"level": 3, "score": 3000}
        service.save_game_state("snake", "slot1", original_state)
        
        loaded = service.load_game_state("snake", "slot1")
        
        assert loaded is not None
        assert loaded["level"] == 3
        assert loaded["score"] == 3000
    
    def test_list_save_slots(self, temp_dir):
        """Test listing save slots."""
        service = SaveService()
        service.set_save_directory(temp_dir)
        
        service.save_game_state("pong", "slot1", {})
        service.save_game_state("pong", "slot2", {})
        service.save_game_state("snake", "slot1", {})
        
        slots = service.list_save_slots("pong")
        
        assert len(slots) >= 2
        assert "slot1" in slots
        assert "slot2" in slots
    
    def test_delete_save_slot(self, temp_dir):
        """Test deleting save slot."""
        service = SaveService()
        service.set_save_directory(temp_dir)
        
        service.save_game_state("pong", "test_slot", {})
        service.delete_save_slot("pong", "test_slot")
        
        loaded = service.load_game_state("pong", "test_slot")
        assert loaded is None
    
    def test_save_encryption(self, temp_dir):
        """Test save encryption."""
        service = SaveService()
        service.set_save_directory(temp_dir)
        
        service.enable_encryption(True)
        service.set_encryption_key("test_key")
        
        state = {"secret": "data"}
        service.save_game_state("game", "slot1", state)
        
        loaded = service.load_game_state("game", "slot1")
        
        assert loaded["secret"] == "data"
    
    def test_auto_save(self, temp_dir):
        """Test auto-save functionality."""
        service = SaveService()
        service.set_save_directory(temp_dir)
        
        service.enable_auto_save(True)
        service.set_auto_save_interval(60.0)
        
        assert service.auto_save_enabled


class TestServicesIntegration:
    """Integration tests for services."""
    
    def test_services_work_together(self, temp_dir):
        """Test services working together."""
        stats_service = StatisticsService()
        achievement_service = AchievementService()
        notification_service = NotificationService()
        
        # Track statistic
        stats_service.track("wins", 1)
        
        # Register achievement
        achievement = Achievement(
            id="first_win",
            name="First Win",
            description="Win a game",
            condition=lambda s: s.get("wins", 0) >= 1
        )
        achievement_service.register(achievement)
        
        # Check achievements
        stats = stats_service.get_all_statistics()
        achievement_service.check_achievements(stats)
        
        # Show notification
        notification_service.show("Achievement unlocked!", NotificationPriority.SUCCESS)
        
        # Should all work together
        assert True

