"""
Módulo que representa un estudiante con sus evaluaciones.
"""

from typing import List
from src.models.evaluation import Evaluation


class Student:
    """
    Representa un estudiante con sus evaluaciones y datos académicos.
    
    Attributes:
        student_id (str): Identificador único del estudiante
        evaluations (List[Evaluation]): Lista de evaluaciones del estudiante
        has_reached_minimum_classes (bool): Indica si cumplió asistencia mínima
    """
    
    MAX_EVALUATIONS = 10  # RNF01: Máximo 10 evaluaciones
    
    def __init__(self, student_id: str):
        """
        Inicializa un estudiante.
        
        Args:
            student_id: Identificador único del estudiante
        """
        self.student_id = student_id
        self.evaluations: List[Evaluation] = []
        self.has_reached_minimum_classes = False
    
    def add_evaluation(self, evaluation: Evaluation) -> None:
        """
        Agrega una evaluación al estudiante.
        
        Args:
            evaluation: Evaluación a agregar
            
        Raises:
            ValueError: Si se excede el límite máximo de evaluaciones (RNF01)
        """
        if len(self.evaluations) >= self.MAX_EVALUATIONS:
            raise ValueError(
                f"No se pueden agregar más de {self.MAX_EVALUATIONS} evaluaciones"
            )
        self.evaluations.append(evaluation)
    
    def get_total_weight(self) -> float:
        """
        Calcula el peso total de todas las evaluaciones.
        
        Returns:
            float: Suma de todos los pesos
        """
        return sum(eval.weight for eval in self.evaluations)
    
    def __repr__(self) -> str:
        return f"Student(id={self.student_id}, evaluations={len(self.evaluations)})"

