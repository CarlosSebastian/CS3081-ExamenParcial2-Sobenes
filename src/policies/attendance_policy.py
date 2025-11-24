"""
Módulo que maneja la política de asistencia mínima.
"""


class AttendancePolicy:
    """
    Política de asistencia mínima según el reglamento académico de UTEC.
    
    Define las penalizaciones aplicadas cuando un estudiante no cumple
    con la asistencia mínima requerida.
    """
    
    PENALTY_NO_ATTENDANCE = 2.0  # Penalización en puntos por no cumplir asistencia
    
    @staticmethod
    def calculate_penalty(has_reached_minimum_classes: bool) -> float:
        """
        Calcula la penalización por no cumplir asistencia mínima.
        
        Args:
            has_reached_minimum_classes: True si cumplió asistencia, False en caso contrario
            
        Returns:
            float: Penalización a aplicar (0 si cumplió, PENALTY_NO_ATTENDANCE si no)
        """
        if has_reached_minimum_classes:
            return 0.0
        return AttendancePolicy.PENALTY_NO_ATTENDANCE
    
    @staticmethod
    def is_attendance_valid(has_reached_minimum_classes: bool) -> bool:
        """
        Verifica si el estudiante cumple con la asistencia mínima.
        
        Args:
            has_reached_minimum_classes: Estado de asistencia del estudiante
            
        Returns:
            bool: True si cumple, False en caso contrario
        """
        return has_reached_minimum_classes

