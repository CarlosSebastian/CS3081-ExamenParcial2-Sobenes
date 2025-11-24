"""
Módulo principal para el cálculo de la nota final del estudiante.
"""

from typing import Dict
from src.models.student import Student
from src.policies.attendance_policy import AttendancePolicy
from src.policies.extra_points_policy import ExtraPointsPolicy


class GradeCalculator:
    """
    Calculadora de nota final que integra evaluaciones, asistencia y puntos extra.
    
    Implementa RF04: Cálculo de nota final considerando:
    - Promedio ponderado de evaluaciones
    - Penalización por inasistencias
    - Puntos extra según política
    """
    
    def __init__(self, attendance_policy: AttendancePolicy, 
                 extra_points_policy: ExtraPointsPolicy):
        """
        Inicializa el calculador de notas.
        
        Args:
            attendance_policy: Política de asistencia a aplicar
            extra_points_policy: Política de puntos extra a aplicar
        """
        self.attendance_policy = attendance_policy
        self.extra_points_policy = extra_points_policy
    
    def calculate_final_grade(self, student: Student, 
                            academic_year: int = 0) -> Dict[str, float]:
        """
        Calcula la nota final del estudiante (RF04).
        
        El cálculo es determinista (RNF03): con los mismos datos de entrada
        siempre genera la misma nota final.
        
        Args:
            student: Estudiante con sus evaluaciones y datos
            academic_year: Año académico para consultar política de puntos extra
            
        Returns:
            Dict con:
                - 'weighted_average': Promedio ponderado
                - 'attendance_penalty': Penalización por asistencia
                - 'extra_points': Puntos extra aplicados
                - 'final_grade': Nota final calculada
                
        Raises:
            ValueError: Si el estudiante no tiene evaluaciones o pesos inválidos
        """
        if not student.evaluations:
            raise ValueError("El estudiante debe tener al menos una evaluación")
        
        total_weight = student.get_total_weight()
        if total_weight == 0:
            raise ValueError("El peso total de las evaluaciones no puede ser cero")
        
        # Calcular promedio ponderado
        weighted_sum = sum(eval.get_weighted_grade() for eval in student.evaluations)
        weighted_average = weighted_sum / (total_weight / 100)
        
        # Aplicar penalización por asistencia
        attendance_penalty = self.attendance_policy.calculate_penalty(
            student.has_reached_minimum_classes
        )
        
        # Obtener puntos extra según política
        extra_points = self.extra_points_policy.get_extra_points_for_year(academic_year)
        
        # Calcular nota final
        final_grade = weighted_average - attendance_penalty + extra_points
        
        # Asegurar que la nota final no sea negativa
        final_grade = max(0.0, final_grade)
        
        return {
            'weighted_average': round(weighted_average, 2),
            'attendance_penalty': round(attendance_penalty, 2),
            'extra_points': round(extra_points, 2),
            'final_grade': round(final_grade, 2)
        }
    
    def get_calculation_details(self, student: Student, 
                               academic_year: int = 0) -> Dict:
        """
        Obtiene el detalle completo del cálculo (RF05).
        
        Args:
            student: Estudiante con sus evaluaciones
            academic_year: Año académico para consultar política
            
        Returns:
            Dict con todos los detalles del cálculo
        """
        calculation = self.calculate_final_grade(student, academic_year)
        
        return {
            'student_id': student.student_id,
            'number_of_evaluations': len(student.evaluations),
            'evaluations': [
                {
                    'grade': eval.grade,
                    'weight': eval.weight,
                    'weighted_grade': round(eval.get_weighted_grade(), 2)
                }
                for eval in student.evaluations
            ],
            'total_weight': round(student.get_total_weight(), 2),
            'has_reached_minimum_classes': student.has_reached_minimum_classes,
            'extra_points_policy_active': self.extra_points_policy.is_extra_points_active(
                academic_year
            ),
            **calculation
        }

