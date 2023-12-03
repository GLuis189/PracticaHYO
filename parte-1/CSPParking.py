import sys
import csv
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
    # print(dimension)

    # La segunda es la disposición de estaciones de carga 
    # Es una lista con tuplas (fila, columna) que indica la posicion de esta
    partes = parking[1][3:].split(')(')
    partes[0] = partes[0][1:]
    partes[-1] = partes[-1][:-1]
    cargas = [tuple(map(int, parte.split(','))) for parte in partes]
    # print(cargas)

    # El resto son ambulancias
    # Es una lista con tuplas de la siguiente manera (ID, TSU/TNU, C/X) ID como entero?
    ambulancias = [(int(partes[0]), partes[1], partes[2]) for partes in (elemento.split('-') for elemento in parking[2:])]
    ambulancias_tsu = [ambulancia for ambulancia in ambulancias if ambulancia[1] == 'TSU']
    # print(ambulancias)
    # print(ambulancias_tsu)
    return dimension, cargas, ambulancias, ambulancias_tsu


def guardar_soluciones(soluciones, dimension, ambulancias):
    # Abrir el archivo CSV en modo escritura
    with open( lectura_parking + '_sol.csv', 'w', newline='') as archivo:
        escritor = csv.writer(archivo, quotechar='"', quoting=csv.QUOTE_ALL, delimiter=',')

        # Escribir el número de soluciones
        escritor.writerow(['N. Sol:', len(soluciones)])

        # Para cada solución
        for solucion in soluciones:
            # Crear una matriz para representar el parking
            parking = [['-']*dimension[1] for _ in range(dimension[0])]

            # Para cada ambulancia en la solución
            for ambulancia in ambulancias:
                # Obtener la plaza asignada a la ambulancia
                plaza = solucion[ambulancia[0]]

                # Colocar la ambulancia en la plaza correspondiente en la matriz
                parking[plaza[0]-1][plaza[1]-1] = '{}-{}-{}'.format(ambulancia[0], ambulancia[1], ambulancia[2])

            # Escribir la matriz en el archivo CSV
            for fila in parking:
                escritor.writerow(fila)
            escritor.writerow([])

dimension, cargas, ambulancias, ambulancias_tsu= leer_archivo()
problem = Problem()

todas_las_plazas = [(i, j) for i in range(1, dimension[0]+1) for j in range(1, dimension[1]+1)]
# Restricción de unicidad: Todo vehículo tiene que tener asignada una plaza y sólo una
for ambulancia in ambulancias:
    if ambulancia[2] == 'C':  # Si el vehículo tiene congelador
        problem.addVariable(ambulancia[0], cargas)  # Solo puede ir a las plazas con conexión eléctrica
    else:
        problem.addVariable(ambulancia[0], todas_las_plazas)

#añade una restricción al problema que indica que todas las ambulancias deben tenerplazas diferentes.
problem.addConstraint(AllDifferentConstraint(), [ambulancia[0] for ambulancia in ambulancias])

# Restricción de TSU: Un vehículo de tipo TSU no puede tener aparcado por delante, en su misma fila, a ningún otro vehículo excepto si éste es también de tipo TSU
def restriccion_tsu(*plazas):
    tsus = [plaza for plaza, ambulancia in zip(plazas, ambulancias) if ambulancia in ambulancias_tsu]
    for tsu in tsus:
        if any(plaza[0] == tsu[0] and plaza[1] > tsu[1] and ambulancia not in ambulancias_tsu for plaza in plazas):
            return False
    return True
problem.addConstraint(restriccion_tsu, [ambulancia[0] for ambulancia in ambulancias])

# Restricción de maniobrabilidad: Todo vehículo debe tener libre una plaza a izquierda o derecha (mirando en dirección a la salida)
def restriccion_maniobrabilidad(*plazas):
    for plaza in plazas:
        # Comprobar si hay ambulancias tanto arriba como abajo
        if any(plaza[1] == otra_plaza[1] and abs(plaza[0] - otra_plaza[0]) == 1 for otra_plaza in plazas if otra_plaza != plaza):
            if plaza[0] == 1 or plaza[0] == dimension[0]:
                return False
            # Si es así, comprobar si al menos uno de los espacios está libre
            if not any(plaza[1] == otra_plaza[1] and abs(plaza[0] - otra_plaza[0]) == 1 for otra_plaza in todas_las_plazas if otra_plaza != plaza):
                 # Si la plaza está en el límite del parking, no considerar la pared como una plaza libre
                return False
    return True
problem.addConstraint(restriccion_maniobrabilidad, [ambulancia[0] for ambulancia in ambulancias])

soluciones = problem.getSolutions()
num_soluciones = len(soluciones)
if num_soluciones == 0:
    print("No se ha encontrado soluciones.")
    exit()

# Llamar a la función guardar_soluciones con las soluciones obtenidas
guardar_soluciones(soluciones, dimension, ambulancias)
