"""
Tests unitarios para la clase Student.
"""

import pytest
from src.models.student import Student
from src.models.evaluation import Evaluation


class TestStudent:
    """Tests para la clase Student."""
    
    def test_shouldCreateStudent_whenValidId(self):
        """Test: Creación exitosa de estudiante."""
        student = Student("ST001")
        assert student.student_id == "ST001"
        assert len(student.evaluations) == 0
        assert student.has_reached_minimum_classes is False
    
    def test_shouldAddEvaluation_whenWithinLimit(self):
        """Test: Agregar evaluación dentro del límite."""
        student = Student("ST002")
        evaluation = Evaluation(15.0, 30.0)
        student.add_evaluation(evaluation)
        
        assert len(student.evaluations) == 1
        assert student.evaluations[0] == evaluation
    
    def test_shouldRaiseError_whenExceedingMaxEvaluations(self):
        """Test: Error al exceder máximo de evaluaciones (RNF01)."""
        student = Student("ST003")
        
        # Agregar 10 evaluaciones (máximo permitido)
        for i in range(Student.MAX_EVALUATIONS):
            student.add_evaluation(Evaluation(15.0, 10.0))
        
        # Intentar agregar una más debe fallar
        with pytest.raises(ValueError, match="No se pueden agregar más de"):
            student.add_evaluation(Evaluation(15.0, 10.0))
    
    def test_shouldCalculateTotalWeight_correctly(self):
        """Test: Cálculo correcto del peso total."""
        student = Student("ST004")
        student.add_evaluation(Evaluation(15.0, 30.0))
        student.add_evaluation(Evaluation(18.0, 40.0))
        student.add_evaluation(Evaluation(16.0, 30.0))
        
        total_weight = student.get_total_weight()
        assert total_weight == 100.0
    
    def test_shouldSetAttendanceStatus(self):
        """Test: Establecer estado de asistencia."""
        student = Student("ST005")
        student.has_reached_minimum_classes = True
        assert student.has_reached_minimum_classes is True
        
        student.has_reached_minimum_classes = False
        assert student.has_reached_minimum_classes is False

