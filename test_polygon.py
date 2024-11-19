from shapely.geometry import Point, Polygon
def is_point_in_any_polygon(coordX, coordY, polygons):
    """
    Verifica si un punto está contenido en alguno de los tres polígonos proporcionados.

    Args:
    coordX (float): Coordenada X del punto.
    coordY (float): Coordenada Y del punto.
    polygons (list of Polygon): Lista de objetos Polygon.

    Returns:
    bool: True si el punto está contenido en alguno de los polígonos, False en caso contrario.
    """
    point = Point(coordX, coordY)
    for polygon in polygons:
        if polygon.distance(point) <= 70:
            return True
    return False

# Ejemplo de uso

coordX = 1190.0
coordY = 479.0


# Coordenadas como cadenas de texto
coordinates = [
   "1092,457", "1320,457", "1092,497", "1320,497"
    ]

# Convertir las coordenadas a tuplas de enteros
coordinates = [tuple(map(int, coord.split(','))) for coord in coordinates]

# Crear el polígono
polygon = Polygon(coordinates)

polygons = [polygon]


print(polygon)

if is_point_in_any_polygon(coordX, coordY, polygons):
    print("El punto está contenido en alguno de los polígonos.")
else:
    print("El punto no está contenido en ninguno de los polígonos.")



def polygon_contains_point(polygon,point):
    """
    Verifica si un punto está contenido en un polígono.

    Args:
    polygon (Polygon): Objeto Polygon.
    point (Point): Objeto Point.

    Returns:
    bool: True si el punto está contenido en el polígono, False en caso contrario.
    """
    return polygon.contains(point)

# Ejemplo de uso
coordinates=["418,370", "678,370", "418,416", "678,416"]
coordinates = [tuple(map(int, coord.split(','))) for coord in coordinates]
print(coordinates)
polygon2 = Polygon(coordinates)
point3 = Point(538, 394)

print (polygon2)
print("el poligono contiene el punto?",polygon_contains_point(polygon2,point3))


# Coordenadas del polígono (en el orden correcto)
vertices = [(418, 370), (678, 370), (678, 416), (418, 416)]
poligono = Polygon(vertices)

# Punto que queremos verificar
punto = Point(538, 394)

# Verificar si el punto está dentro del polígono
if poligono.contains(punto):
    print("El punto está dentro del polígono.")
else:
    print("El punto está fuera del polígono.")