import sys
from constraint import *

lectura_parking  = sys.argv[1]

def leer_archivo():
    # Leer el archivo de entrada
    parking = [] 
    with open(lectura_parking, "r") as f:
        for linea in f:
            parking.append(linea.strip())
    #print(parking)

    # Crear las variables para el programa

    # La primera linea es la dimension del parking 
    # Es una tupla (filas, columnas)
    dimension = parking[0].split("x")
    dimension = tuple(int(d) for d in dimension)
    print(dimension)

    # La segunda es la disposición de estaciones de carga 
    # Es una lista con tuplas (fila, columna) que indica la posicion de esta
    partes = parking[1][3:].split(')(')
    partes[0] = partes[0][1:]
    partes[-1] = partes[-1][:-1]
    cargas = [tuple(map(int, parte.split(','))) for parte in partes]
    print(cargas)

    # El resto son ambulancias
    # Es una lista con tuplas de la siguiente manera (ID, TSU/TNU, C/X) ID como entero?
    ambulancias = [(int(partes[0]), partes[1], partes[2]) for partes in (elemento.split('-') for elemento in parking[2:])]
    print(ambulancias)

    return dimension, cargas, ambulancias



dimension, cargas, ambulancias = leer_archivo()
problem = Problem()

todas_las_plazas = [(i, j) for i in range(1, dimension[0]+1) for j in range(1, dimension[1]+1)]
 # Restricción de unicidad: Todo vehículo tiene que tener asignada una plaza y sólo una
for ambulancia in ambulancias:
    if ambulancia[2] == 'C':  # Si el vehículo tiene congelador
        problem.addVariable(ambulancia[0], cargas)  # Solo puede ir a las plazas con conexión eléctrica
    else:
        problem.addVariable(ambulancia[0], todas_las_plazas)

#añade una restricción al problema que indica que todas las variables (en este caso, las ambulancias) deben tener valores diferentes (es decir, plazas de parking diferentes).
problem.addConstraint(AllDifferentConstraint(), [ambulancia[0] for ambulancia in ambulancias])

# Restricción de TSU: Un vehículo de tipo TSU no puede tener aparcado por delante, en su misma fila, a ningún otro vehículo excepto si éste es también de tipo TSU
def restriccion_tsu(*plazas):
    tsus = [plaza for plaza, ambulancia in zip(plazas, ambulancias) if ambulancia[1] == 'TSU']
    for tsu in tsus:
        if any(plaza[0] == tsu[0] and plaza[1] > tsu[1] and ambulancias[plazas.index(plaza)][1] != 'TSU' for plaza in plazas):
            return False
    return True
problem.addConstraint(restriccion_tsu, [ambulancia[0] for ambulancia in ambulancias])

# Restricción de maniobrabilidad: Todo vehículo debe tener libre una plaza a izquierda o derecha (mirando en dirección a la salida)
def restriccion_maniobrabilidad(*plazas):
    for plaza in plazas:
        if any(plaza[0] == otra_plaza[0] and abs(plaza[1] - otra_plaza[1]) == 1 for otra_plaza in plazas if otra_plaza != plaza):
            return False
    return True
problem.addConstraint(restriccion_maniobrabilidad, [ambulancia[0] for ambulancia in ambulancias])

soluciones = problem.getSolutions()

print(soluciones)

''' problem = Problem()
for i in range(dimension[0]):
    for j in range(dimension[1]):
        problem.addVariable("X{}{}".format(i,j), list(range(len(ambulancias) + 1))[1:] + ["-"]) '''

