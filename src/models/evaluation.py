"""
Módulo que representa una evaluación individual de un estudiante.
"""


class Evaluation:
    """
    Representa una evaluación con su nota y peso porcentual.
    
    Attributes:
        grade (float): Nota obtenida en la evaluación (0-20 típicamente)
        weight (float): Porcentaje de peso sobre la nota final (0-100)
    """
    
    def __init__(self, grade: float, weight: float):
        """
        Inicializa una evaluación.
        
        Args:
            grade: Nota obtenida (debe ser >= 0)
            weight: Porcentaje de peso (debe estar entre 0 y 100)
            
        Raises:
            ValueError: Si grade o weight son inválidos
        """
        if grade < 0:
            raise ValueError("La nota no puede ser negativa")
        if weight < 0 or weight > 100:
            raise ValueError("El peso debe estar entre 0 y 100")
        
        self.grade = grade
        self.weight = weight
    
    def get_weighted_grade(self) -> float:
        """
        Calcula la nota ponderada (nota * peso).
        
        Returns:
            float: Nota ponderada
        """
        return self.grade * (self.weight / 100)
    
    def __repr__(self) -> str:
        return f"Evaluation(grade={self.grade}, weight={self.weight}%)"

