import math


class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def compute_distance(self, point: "Point") -> float:
        """Calcula la distancia entre dos puntos."""
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Line:
    """Plantilla para representar una línea en un plano."""
    def __init__(self, point1: "Point", point2: "Point") -> None:
        self.point1 = point1
        self.point2 = point2
        self.length = self.compute_length()
        self.slope = self.compute_slope()
        self.line_points = []

    def compute_length(self) -> float:
        """Retorna la longitud de la línea."""
        length: float = ((self.point1.x - self.point2.x)**2 + (self.point1.y - self.point2.y)**2)**0.5
        return length

    def compute_slope(self):
        """Retorna en grados la pendiente de la línea."""
        co: int = abs(self.point1.y - self.point2.y)
        ca: int = abs(self.point1.x - self.point2.x)
        self.slope = (math.atan2(co, ca)) * (180/math.pi)
        return self.slope

    def compute_horizontal_cross(self) -> bool:
        """Verifica si hay intersección con el eje x."""
        if self.point1.y * self.point2.y <= 0:
            return True
        return False

    def compute_vertical_cross(self):
        """Verifica si hay intersección con el eje y."""
        if self.point1.x * self.point2.x <= 0:
            return True
        return False

    def discretize_line(self, n: int) -> list[str]:
        """Divide la línea en 'n' puntos distribuidos uniformemente."""
        self.line_points: list["Point"] = []

        # Hallar la distancia entre puntos
        distance_x: float = (self.point2.x-self.point1.x) / (n-1)
        distance_y: float = (self.point2.y-self.point1.y) / (n-1)
        # Crear n puntos
        for i in range(n):
            new_x: float = self.point1.x + (i * distance_x)
            new_y: float = self.point1.y + (i * distance_y)
            new_point = Point(new_x, new_y)
            self.line_points.append(new_point)

        return [str(point) for point in self.line_points]

    def __str__(self) -> str:
        return f"({self.point1.x}, {self.point1.y}) - ({self.point2.x}, {self.point2.y})"


class Rectangle:
    def __init__(self, method: int, *args):
        match method:
            case 1:
                # Caso esquina: esquina inferior izquierda, ancho y altura
                self.bl_corner, self.width, self.height = args
                new_x = (self.bl_corner.x + self.width) / 2
                new_y = (self.bl_corner.y + self.height) / 2
                self.center = Point(new_x, new_y)

            case 2:
                # Caso centro: centro, ancho y altura
                self.center, self.width, self.height = args

            case 3:
                # Caso esquinas opuestas
                self.corner1, self.corner2 = args

                if self.corner1.x == self.corner2.x and self.corner1.y == self.corner2.y:
                    raise ValueError("Seleccione puntos en diferentes ubicaciones del espacio.")

                self.width = abs(self.corner2.x - self.corner1.x)
                self.height = abs(self.corner2.y - self.corner1.y)

            case 4:
                # Caso definido por líneas
                self.line1, self.line2, self.line3, self.line4 = args
                opposite_lines = []

                for i in range(len(args)):
                    line = args[i]
                    x1, y1 = line.point1.x, line.point1.y
                    x2, y2 = line.point2.x, line.point2.y

                    for j in range(i + 1, len(args)):
                        next_line = args[j]
                        x3, y3 = next_line.point1.x, next_line.point1.y
                        x4, y4 = next_line.point2.x, next_line.point2.y

                        # Verificar puntos adyacentes
                        if not (
                            (x1 == x3 and y1 == y3) or (x1 == x4 and y1 == y4) or
                            (x2 == x3 and y2 == y3) or (x2 == x4 and y2 == y4)
                        ):
                            opposite_lines.append((line, next_line))

                if len(opposite_lines) != 2:
                    raise ValueError("Introduzca líneas que formen un rectángulo.")

                # Verificar propiedades del rectángulo
                line1, line3 = opposite_lines[0]
                line2, line4 = opposite_lines[1]

                conditions = [
                    line1.compute_length() == line3.compute_length(),
                    line2.compute_length() == line4.compute_length(),
                    line1.compute_slope() == line3.compute_slope(),
                    line2.compute_slope() == line4.compute_slope()
                ]

                if not all(conditions):
                    raise ValueError("Introduzca líneas que formen un rectángulo.")

                # Calcular ancho y altura
                self.width = line1.compute_length()
                self.height = line2.compute_length()

            case _:
                raise ValueError("Ningún método seleccionado.")

    def compute_area(self) -> float:
        """Calcula el área del rectángulo."""
        return self.width * self.height

    def compute_perimeter(self) -> float:
        """Calcula el perímetro del rectángulo."""
        return 2 * (self.width + self.height)

    def compute_interference_point(self, point: "Point") -> bool:
        """Verifica si un punto está dentro del rectángulo."""
        start_x, end_x = self.compute_width_range()
        start_y, end_y = self.compute_height_range()
        return (start_x <= point.x <= end_x) and (start_y <= point.y <= end_y)

    def compute_width_range(self) -> list[float]:
        """Obtiene el rango horizontal del rectángulo."""
        half_width = self.width / 2
        return [self.center.x - half_width, self.center.x + half_width]

    def compute_height_range(self) -> list[float]:
        """Obtiene el rango vertical del rectángulo."""
        half_height = self.height / 2
        return [self.center.y - half_height, self.center.y + half_height]

    def compute_interference_line(self, line: "Line") -> bool:
        """Verifica si una línea está dentro del rectángulo."""
        # Verificar si alguno de los extremos de la línea está dentro del rectángulo
        return (
            self.compute_interference_point(line.point1) or
            self.compute_interference_point(line.point2)
        )


class Square(Rectangle):
    def __init__(self, method: int, *args):
        # Se llama a la clase padre y se inicializa
        if method == 1:
            super().__init__(1, args[0], args[1], args[1])
        elif method == 2:
            super().__init__(2, args[0], args[1], args[1])
        elif method == 3:
            super().__init__(3, args[0], args[1])


line1 = Line(Point(4, 5), Point(-3, 10))
print(line1.compute_vertical_cross())
print(line1.compute_slope())
print(line1.compute_length())
print(line1.discretize_line(5))

# Bottom-Left corner + Width + Height
r1 = Rectangle(1, Point(), 10, 5)

# Center + Width + Height
r2 = Rectangle(2, Point(), 10, 5)

# Opposite corners
r3 = Rectangle(3, Point(), Point(2, 2))

# 4 Lines
line1 = Line(Point(), Point(0,5))
line2 = Line(Point(0,5), Point(5, 5))
line3 = Line(Point(5,5), Point(5, 0))
line4 = Line(Point(5, 0), Point())
r4 = Rectangle(4, line1, line2, line3, line4)

print(r1.compute_perimeter())
# (10+5) * 2

print(r2.compute_interference_point(Point(3, 6)))
# Max_height = 2.5 from (0, 0), height = 5

print(r3.compute_area())
# Width = 2 ; Height = 2
