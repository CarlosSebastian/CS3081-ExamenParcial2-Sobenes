"""
Aplicación principal para el cálculo de notas finales.
Sistema: CS-GradeCalculator
Actor: Docente UTEC
Caso de Uso: CU001 - Calcular nota final del estudiante
"""

from src.models.student import Student
from src.models.evaluation import Evaluation
from src.policies.attendance_policy import AttendancePolicy
from src.policies.extra_points_policy import ExtraPointsPolicy
from src.calculator.grade_calculator import GradeCalculator


def main():
    """
    Función principal que ejecuta el caso de uso CU001.
    """
    print("=" * 60)
    print("Sistema: CS-GradeCalculator")
    print("Caso de Uso: CU001 - Calcular nota final del estudiante")
    print("=" * 60)
    print()
    
    # Solicitar datos del estudiante
    student_id = input("Ingrese el código o identificador del estudiante: ").strip()
    student = Student(student_id)
    
    # Registrar evaluaciones (RF01)
    print("\n--- Registro de Evaluaciones (RF01) ---")
    print(f"Máximo de evaluaciones permitidas: {Student.MAX_EVALUATIONS}")
    
    while True:
        try:
            num_evaluations = int(input("¿Cuántas evaluaciones desea registrar? "))
            if num_evaluations < 1:
                print("Debe registrar al menos una evaluación.")
                continue
            if num_evaluations > Student.MAX_EVALUATIONS:
                print(f"No se pueden registrar más de {Student.MAX_EVALUATIONS} evaluaciones.")
                continue
            break
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    for i in range(num_evaluations):
        print(f"\nEvaluación {i + 1}:")
        while True:
            try:
                grade = float(input("  Nota obtenida: "))
                weight = float(input("  Porcentaje de peso (0-100): "))
                evaluation = Evaluation(grade, weight)
                student.add_evaluation(evaluation)
                break
            except ValueError as e:
                print(f"  Error: {e}")
    
    # Registrar asistencia mínima (RF02)
    print("\n--- Registro de Asistencia Mínima (RF02) ---")
    while True:
        attendance_input = input(
            "¿El estudiante cumplió la asistencia mínima? (s/n): "
        ).strip().lower()
        if attendance_input in ['s', 'si', 'sí', 'y', 'yes']:
            student.has_reached_minimum_classes = True
            break
        elif attendance_input in ['n', 'no']:
            student.has_reached_minimum_classes = False
            break
        else:
            print("Por favor, responda 's' o 'n'.")
    
    # Consultar política de puntos extra (RF03)
    print("\n--- Política de Puntos Extra (RF03) ---")
    print("Ingrese la política de puntos extra por año académico.")
    print("Para cada año, indique si los docentes están de acuerdo (s/n).")
    
    all_years_teachers = []
    while True:
        try:
            num_years = int(input("¿Cuántos años académicos desea configurar? "))
            if num_years < 1:
                print("Debe haber al menos un año académico.")
                continue
            break
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    for year in range(num_years):
        while True:
            year_input = input(
                f"  Año académico {year + 1}: ¿Docentes de acuerdo? (s/n): "
            ).strip().lower()
            if year_input in ['s', 'si', 'sí', 'y', 'yes']:
                all_years_teachers.append(True)
                break
            elif year_input in ['n', 'no']:
                all_years_teachers.append(False)
                break
            else:
                print("    Por favor, responda 's' o 'n'.")
    
    # Configurar políticas y calculadora
    attendance_policy = AttendancePolicy()
    extra_points_policy = ExtraPointsPolicy(all_years_teachers)
    calculator = GradeCalculator(attendance_policy, extra_points_policy)
    
    # Solicitar año académico para el cálculo
    while True:
        try:
            academic_year = int(
                input(f"\n¿Para qué año académico desea calcular? (1-{num_years}): ")
            ) - 1
            if 0 <= academic_year < num_years:
                break
            else:
                print(f"Por favor, ingrese un número entre 1 y {num_years}.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    # Calcular nota final (RF04)
    print("\n" + "=" * 60)
    print("--- Cálculo de Nota Final (RF04) ---")
    print("=" * 60)
    
    try:
        calculation_details = calculator.get_calculation_details(student, academic_year)
        
        # Mostrar detalle del cálculo (RF05)
        print("\n--- Detalle del Cálculo (RF05) ---")
        print(f"Estudiante: {calculation_details['student_id']}")
        print(f"Número de evaluaciones: {calculation_details['number_of_evaluations']}")
        print(f"\nEvaluaciones:")
        for i, eval_data in enumerate(calculation_details['evaluations'], 1):
            print(f"  {i}. Nota: {eval_data['grade']}, "
                  f"Peso: {eval_data['weight']}%, "
                  f"Ponderado: {eval_data['weighted_grade']}")
        
        print(f"\nPeso total: {calculation_details['total_weight']}%")
        print(f"Asistencia mínima cumplida: "
              f"{'Sí' if calculation_details['has_reached_minimum_classes'] else 'No'}")
        print(f"Política de puntos extra activa: "
              f"{'Sí' if calculation_details['extra_points_policy_active'] else 'No'}")
        
        print(f"\n--- Resultados del Cálculo ---")
        print(f"Promedio ponderado: {calculation_details['weighted_average']}")
        print(f"Penalización por inasistencias: {calculation_details['attendance_penalty']}")
        print(f"Puntos extra aplicados: {calculation_details['extra_points']}")
        print(f"\n{'=' * 60}")
        print(f"NOTA FINAL: {calculation_details['final_grade']}")
        print(f"{'=' * 60}")
        
    except ValueError as e:
        print(f"Error en el cálculo: {e}")


if __name__ == "__main__":
    main()

