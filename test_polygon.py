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
polygons = [
    Polygon([(472, 315), (625, 315), (472, 336), (472, 315)]),
    Polygon([(421, 375), (670, 375), (421, 408), (670, 408)]),

]

coordX = 597.76
coordY = 433.12



if is_point_in_any_polygon(coordX, coordY, polygons):
    print("El punto está contenido en alguno de los polígonos.")
else:
    print("El punto no está contenido en ninguno de los polígonos.")