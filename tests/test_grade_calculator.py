"""
Tests unitarios para GradeCalculator.
Cubre casos normales, sin asistencia, con/sin puntos extra y casos borde.
"""

import pytest
from src.models.student import Student
from src.models.evaluation import Evaluation
from src.policies.attendance_policy import AttendancePolicy
from src.policies.extra_points_policy import ExtraPointsPolicy
from src.calculator.grade_calculator import GradeCalculator


class TestGradeCalculatorNormal:
    """Tests para cálculo normal con asistencia mínima cumplida."""
    
    def test_shouldReturnCorrectFinalGrade_whenStudentHasEvaluationsAndAttendance(self):
        """Test: Cálculo normal con evaluaciones y asistencia cumplida."""
        student = Student("ST001")
        student.add_evaluation(Evaluation(15.0, 30.0))
        student.add_evaluation(Evaluation(18.0, 40.0))
        student.add_evaluation(Evaluation(16.0, 30.0))
        student.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        result = calculator.calculate_final_grade(student, 0)
        
        # Promedio ponderado: (15*0.3 + 18*0.4 + 16*0.3) = 4.5 + 7.2 + 4.8 = 16.5
        assert result['weighted_average'] == 16.5
        assert result['attendance_penalty'] == 0.0
        assert result['extra_points'] == 0.0
        assert result['final_grade'] == 16.5
    
    def test_shouldReturnCorrectFinalGrade_whenSingleEvaluation(self):
        """Test: Cálculo con una sola evaluación."""
        student = Student("ST002")
        student.add_evaluation(Evaluation(20.0, 100.0))
        student.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        result = calculator.calculate_final_grade(student, 0)
        
        assert result['weighted_average'] == 20.0
        assert result['final_grade'] == 20.0


class TestGradeCalculatorWithoutAttendance:
    """Tests para caso sin asistencia mínima."""
    
    def test_shouldApplyPenalty_whenStudentDoesNotMeetMinimumAttendance(self):
        """Test: Penalización aplicada cuando no cumple asistencia mínima."""
        student = Student("ST003")
        student.add_evaluation(Evaluation(15.0, 50.0))
        student.add_evaluation(Evaluation(18.0, 50.0))
        student.has_reached_minimum_classes = False
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        result = calculator.calculate_final_grade(student, 0)
        
        # Promedio: (15*0.5 + 18*0.5) = 16.5
        # Penalización: 2.0
        # Nota final: 16.5 - 2.0 = 14.5
        assert result['weighted_average'] == 16.5
        assert result['attendance_penalty'] == 2.0
        assert result['final_grade'] == 14.5


class TestGradeCalculatorWithExtraPoints:
    """Tests para casos con y sin puntos extra."""
    
    def test_shouldApplyExtraPoints_whenPolicyIsActive(self):
        """Test: Puntos extra aplicados cuando la política está activa."""
        student = Student("ST004")
        student.add_evaluation(Evaluation(14.0, 100.0))
        student.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([True, False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        result = calculator.calculate_final_grade(student, 0)
        
        # Promedio: 14.0
        # Puntos extra: 1.0 (año 0 está activo)
        # Nota final: 14.0 + 1.0 = 15.0
        assert result['weighted_average'] == 14.0
        assert result['extra_points'] == 1.0
        assert result['final_grade'] == 15.0
    
    def test_shouldNotApplyExtraPoints_whenPolicyIsInactive(self):
        """Test: Sin puntos extra cuando la política está inactiva."""
        student = Student("ST005")
        student.add_evaluation(Evaluation(14.0, 100.0))
        student.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([False, True])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        result = calculator.calculate_final_grade(student, 0)
        
        # Año 0 inactivo, no puntos extra
        assert result['extra_points'] == 0.0
        assert result['final_grade'] == 14.0
    
    def test_shouldApplyExtraPointsAndPenalty_whenBothConditions(self):
        """Test: Puntos extra y penalización aplicados simultáneamente."""
        student = Student("ST006")
        student.add_evaluation(Evaluation(15.0, 100.0))
        student.has_reached_minimum_classes = False
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([True])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        result = calculator.calculate_final_grade(student, 0)
        
        # Promedio: 15.0
        # Penalización: 2.0
        # Puntos extra: 1.0
        # Nota final: 15.0 - 2.0 + 1.0 = 14.0
        assert result['weighted_average'] == 15.0
        assert result['attendance_penalty'] == 2.0
        assert result['extra_points'] == 1.0
        assert result['final_grade'] == 14.0


class TestGradeCalculatorEdgeCases:
    """Tests para casos borde."""
    
    def test_shouldRaiseError_whenNoEvaluations(self):
        """Test: Error cuando no hay evaluaciones."""
        student = Student("ST007")
        student.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        with pytest.raises(ValueError, match="debe tener al menos una evaluación"):
            calculator.calculate_final_grade(student, 0)
    
    def test_shouldRaiseError_whenTotalWeightIsZero(self):
        """Test: Error cuando el peso total es cero."""
        student = Student("ST008")
        student.add_evaluation(Evaluation(15.0, 0.0))
        student.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        with pytest.raises(ValueError, match="peso total.*no puede ser cero"):
            calculator.calculate_final_grade(student, 0)
    
    def test_shouldHandleZeroGrade(self):
        """Test: Manejo de nota cero."""
        student = Student("ST009")
        student.add_evaluation(Evaluation(0.0, 100.0))
        student.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        result = calculator.calculate_final_grade(student, 0)
        assert result['final_grade'] == 0.0
    
    def test_shouldNotReturnNegativeGrade_whenPenaltyExceedsAverage(self):
        """Test: Nota final no puede ser negativa."""
        student = Student("ST010")
        student.add_evaluation(Evaluation(1.0, 100.0))
        student.has_reached_minimum_classes = False
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        result = calculator.calculate_final_grade(student, 0)
        # 1.0 - 2.0 = -1.0, pero debe ser 0.0
        assert result['final_grade'] == 0.0
    
    def test_shouldHandleInvalidAcademicYear(self):
        """Test: Manejo de año académico inválido."""
        student = Student("ST011")
        student.add_evaluation(Evaluation(15.0, 100.0))
        student.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([True])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        # Año académico fuera de rango
        result = calculator.calculate_final_grade(student, 5)
        assert result['extra_points'] == 0.0


class TestGradeCalculatorDeterministic:
    """Tests para verificar determinismo del cálculo (RNF03)."""
    
    def test_shouldReturnSameResult_whenSameInputs(self):
        """Test: Cálculo determinista - mismos datos, mismo resultado."""
        student1 = Student("ST012")
        student1.add_evaluation(Evaluation(15.0, 50.0))
        student1.add_evaluation(Evaluation(18.0, 50.0))
        student1.has_reached_minimum_classes = True
        
        student2 = Student("ST013")
        student2.add_evaluation(Evaluation(15.0, 50.0))
        student2.add_evaluation(Evaluation(18.0, 50.0))
        student2.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        result1 = calculator.calculate_final_grade(student1, 0)
        result2 = calculator.calculate_final_grade(student2, 0)
        
        assert result1 == result2


class TestGradeCalculatorDetails:
    """Tests para el detalle del cálculo (RF05)."""
    
    def test_shouldReturnCompleteDetails_whenRequested(self):
        """Test: Detalle completo del cálculo."""
        student = Student("ST014")
        student.add_evaluation(Evaluation(15.0, 50.0))
        student.add_evaluation(Evaluation(18.0, 50.0))
        student.has_reached_minimum_classes = True
        
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy([True])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)
        
        details = calculator.get_calculation_details(student, 0)
        
        assert details['student_id'] == "ST014"
        assert details['number_of_evaluations'] == 2
        assert len(details['evaluations']) == 2
        assert 'weighted_average' in details
        assert 'attendance_penalty' in details
        assert 'extra_points' in details
        assert 'final_grade' in details
        assert details['has_reached_minimum_classes'] is True
        assert details['extra_points_policy_active'] is True

