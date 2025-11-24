"""
Tests unitarios para la clase Evaluation.
"""

import pytest
from src.models.evaluation import Evaluation


class TestEvaluation:
    """Tests para la clase Evaluation."""
    
    def test_shouldCreateEvaluation_whenValidData(self):
        """Test: Creación exitosa con datos válidos."""
        evaluation = Evaluation(15.0, 30.0)
        assert evaluation.grade == 15.0
        assert evaluation.weight == 30.0
    
    def test_shouldCalculateWeightedGrade_correctly(self):
        """Test: Cálculo correcto de nota ponderada."""
        evaluation = Evaluation(20.0, 50.0)
        weighted = evaluation.get_weighted_grade()
        # 20.0 * (50.0 / 100) = 10.0
        assert weighted == 10.0
    
    def test_shouldRaiseError_whenNegativeGrade(self):
        """Test: Error con nota negativa."""
        with pytest.raises(ValueError, match="no puede ser negativa"):
            Evaluation(-1.0, 30.0)
    
    def test_shouldRaiseError_whenWeightOutOfRange(self):
        """Test: Error con peso fuera de rango."""
        with pytest.raises(ValueError, match="peso debe estar entre 0 y 100"):
            Evaluation(15.0, 150.0)
        
        with pytest.raises(ValueError, match="peso debe estar entre 0 y 100"):
            Evaluation(15.0, -10.0)
    
    def test_shouldAllowZeroGrade(self):
        """Test: Permite nota cero."""
        evaluation = Evaluation(0.0, 30.0)
        assert evaluation.grade == 0.0
        assert evaluation.get_weighted_grade() == 0.0
    
    def test_shouldAllowZeroWeight(self):
        """Test: Permite peso cero."""
        evaluation = Evaluation(15.0, 0.0)
        assert evaluation.weight == 0.0
        assert evaluation.get_weighted_grade() == 0.0

