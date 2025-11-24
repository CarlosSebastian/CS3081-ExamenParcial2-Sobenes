"""
Tests unitarios para ExtraPointsPolicy.
"""

import pytest
from src.policies.extra_points_policy import ExtraPointsPolicy


class TestExtraPointsPolicy:
    """Tests para la política de puntos extra."""
    
    def test_shouldCreatePolicy_whenValidList(self):
        """Test: Creación exitosa con lista válida."""
        policy = ExtraPointsPolicy([True, False, True])
        assert len(policy.all_years_teachers) == 3
    
    def test_shouldRaiseError_whenInvalidInput(self):
        """Test: Error con entrada inválida."""
        with pytest.raises(ValueError, match="debe ser una lista"):
            ExtraPointsPolicy("not a list")
    
    def test_shouldReturnExtraPoints_whenPolicyActive(self):
        """Test: Puntos extra cuando la política está activa."""
        policy = ExtraPointsPolicy([True, False])
        extra_points = policy.get_extra_points_for_year(0)
        assert extra_points == ExtraPointsPolicy.EXTRA_POINTS_AMOUNT
    
    def test_shouldReturnZero_whenPolicyInactive(self):
        """Test: Sin puntos extra cuando la política está inactiva."""
        policy = ExtraPointsPolicy([False, True])
        extra_points = policy.get_extra_points_for_year(0)
        assert extra_points == 0.0
    
    def test_shouldReturnZero_whenInvalidYear(self):
        """Test: Sin puntos extra para año inválido."""
        policy = ExtraPointsPolicy([True])
        extra_points = policy.get_extra_points_for_year(5)
        assert extra_points == 0.0
        
        extra_points = policy.get_extra_points_for_year(-1)
        assert extra_points == 0.0
    
    def test_shouldCheckPolicyActive_correctly(self):
        """Test: Verificación correcta de política activa."""
        policy = ExtraPointsPolicy([True, False])
        assert policy.is_extra_points_active(0) is True
        assert policy.is_extra_points_active(1) is False
        assert policy.is_extra_points_active(5) is False

