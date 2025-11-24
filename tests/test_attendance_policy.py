"""
Tests unitarios para AttendancePolicy.
"""

from src.policies.attendance_policy import AttendancePolicy


class TestAttendancePolicy:
    """Tests para la política de asistencia."""
    
    def test_shouldReturnZeroPenalty_whenAttendanceMet(self):
        """Test: Sin penalización cuando se cumple asistencia."""
        penalty = AttendancePolicy.calculate_penalty(True)
        assert penalty == 0.0
    
    def test_shouldReturnPenalty_whenAttendanceNotMet(self):
        """Test: Penalización aplicada cuando no se cumple asistencia."""
        penalty = AttendancePolicy.calculate_penalty(False)
        assert penalty == AttendancePolicy.PENALTY_NO_ATTENDANCE
    
    def test_shouldValidateAttendance_correctly(self):
        """Test: Validación correcta de asistencia."""
        assert AttendancePolicy.is_attendance_valid(True) is True
        assert AttendancePolicy.is_attendance_valid(False) is False

