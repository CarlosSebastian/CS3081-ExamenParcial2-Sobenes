"""
Módulo que maneja la política de puntos extra por año académico.
"""

from typing import List


class ExtraPointsPolicy:
    """
    Política de puntos extra definida colectivamente por los docentes.
    
    La política se define por año académico mediante la lista allYearsTeachers,
    donde cada elemento indica si los docentes están de acuerdo en otorgar
    puntos extra para ese año.
    """
    
    EXTRA_POINTS_AMOUNT = 1.0  # Puntos extra a otorgar cuando la política está activa
    
    def __init__(self, all_years_teachers: List[bool]):
        """
        Inicializa la política de puntos extra.
        
        Args:
            all_years_teachers: Lista de booleanos por año académico
                                (True = docentes de acuerdo, False = no de acuerdo)
        """
        if not isinstance(all_years_teachers, list):
            raise ValueError("all_years_teachers debe ser una lista")
        self.all_years_teachers = all_years_teachers
    
    def get_extra_points_for_year(self, academic_year: int) -> float:
        """
        Obtiene los puntos extra para un año académico específico.
        
        Args:
            academic_year: Índice del año académico (0-based)
            
        Returns:
            float: Puntos extra a aplicar (EXTRA_POINTS_AMOUNT si está activo, 0 si no)
        """
        if academic_year < 0 or academic_year >= len(self.all_years_teachers):
            return 0.0
        
        if self.all_years_teachers[academic_year]:
            return ExtraPointsPolicy.EXTRA_POINTS_AMOUNT
        return 0.0
    
    def is_extra_points_active(self, academic_year: int) -> bool:
        """
        Verifica si la política de puntos extra está activa para un año.
        
        Args:
            academic_year: Índice del año académico
            
        Returns:
            bool: True si está activa, False en caso contrario
        """
        if academic_year < 0 or academic_year >= len(self.all_years_teachers):
            return False
        return self.all_years_teachers[academic_year]

