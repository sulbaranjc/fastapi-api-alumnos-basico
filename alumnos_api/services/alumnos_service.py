def calcular_promedio(n1: float, n2: float, n3: float, examen: float) -> float:
    continua = (n1 + n2 + n3) / 3.0
    return round(continua * 0.7 + examen * 0.3, 2)
