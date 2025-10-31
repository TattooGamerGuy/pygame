"""Test scoring system with TDD approach."""

import pytest
from hub.games.space_invaders.constants import (
    ENEMY_TYPE1_SCORE, ENEMY_TYPE2_SCORE, ENEMY_TYPE3_SCORE, WAVE_CLEAR_BONUS
)


class TestScoring:
    """Test scoring mechanics."""
    
    def test_enemy_type1_score(self):
        """Type 1 enemy should give correct points."""
        assert ENEMY_TYPE1_SCORE == 30, f"Type 1 should give 30 points, got {ENEMY_TYPE1_SCORE}"
    
    def test_enemy_type2_score(self):
        """Type 2 enemy should give correct points."""
        assert ENEMY_TYPE2_SCORE == 20, f"Type 2 should give 20 points, got {ENEMY_TYPE2_SCORE}"
    
    def test_enemy_type3_score(self):
        """Type 3 enemy should give correct points."""
        assert ENEMY_TYPE3_SCORE == 10, f"Type 3 should give 10 points, got {ENEMY_TYPE3_SCORE}"
    
    def test_wave_clear_bonus(self):
        """Wave clear should give bonus points."""
        assert WAVE_CLEAR_BONUS == 1000, f"Wave clear should give 1000 points, got {WAVE_CLEAR_BONUS}"
    
    def test_scoring_progression(self):
        """Higher tier enemies should give more points."""
        assert ENEMY_TYPE1_SCORE > ENEMY_TYPE2_SCORE > ENEMY_TYPE3_SCORE, \
            "Scoring should be progressive (type 1 > type 2 > type 3)"

