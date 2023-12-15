import sys
import csv
from constraint import *
import random
import datetime

lectura_parking  = sys.argv[1]
antes = datetime.datetime.now()
def leer_archivo():
    # Leer el archivo de entrada
    parking = [] 
    with open(lectura_parking, "r") as f:
        for linea in f:
            parking.append(linea.strip())

    # Crear las variables para el programa
    # La primera linea es la dimension del parking 
    # Es una tupla (filas, columnas)
    dimension = parking[0].split("x")
    dimension = tuple(int(d) for d in dimension)

    # La segunda es la disposición de estaciones de carga 
    # Es una lista con tuplas (fila, columna) que indica la posicion de esta
    partes = parking[1][3:].split(')(')
    partes[0] = partes[0][1:]
    partes[-1] = partes[-1][:-1]
    cargas = [tuple(map(int, parte.split(','))) for parte in partes]

    # El resto son ambulancias
    # Es una lista con cadenas de caracteres que representan las ambulancias de la siguiente forma: 'ID-TSU/TNU-C/X'
    ambulancias = [(int(partes[0]), partes[1], partes[2]) for partes in (elemento.split('-') for elemento in parking[2:])]
    ambulancias_tsu = [ambulancia for ambulancia in ambulancias if ambulancia[1] == 'TSU']
    ambulancias = [f"{ambulancia[0]}-{ambulancia[1]}-{ambulancia[2]}" for ambulancia in ambulancias]
    ambulancias_tsu = [f"{ambulancia[0]}-{ambulancia[1]}-{ambulancia[2]}" for ambulancia in ambulancias_tsu]
    return dimension, cargas, ambulancias, ambulancias_tsu


def guardar_soluciones(soluciones, dimension, ambulancias):
    # Abrir el archivo CSV en modo escritura
    with open( lectura_parking + '_sol.csv', 'w', newline='', encoding='windows-1252') as archivo:
        escritor = csv.writer(archivo, quotechar='"', quoting=csv.QUOTE_ALL, delimiter=',')

        # Escribir el número de soluciones
        escritor.writerow(['N. Sol:', len(soluciones)])

        # Para cada solución
        sol1 = random.randint(0, len(soluciones)-1)
        sol2 = random.randint(0, len(soluciones)-1)
        sol3 = random.randint(0, len(soluciones)-1)
        
        contador = 0
        for solucion in soluciones:
            if contador == sol1 or contador == sol2 or contador == sol3:
                escritor.writerow([])
                # Crear una matriz para representar el parking
                parking = [['-']*dimension[1] for _ in range(dimension[0])]

                # Para cada ambulancia en la solución
                for ambulancia in ambulancias:
                    # Obtener la plaza asignada a la ambulancia
                    plaza = solucion[ambulancia]

                    # Colocar la ambulancia en la plaza correspondiente en la matriz
                    parking[plaza[0]-1][plaza[1]-1] = ambulancia

                # Escribir la matriz en el archivo CSV
                for fila in parking:
                    escritor.writerow(fila)
        
            contador += 1
            

dimension, cargas, ambulancias, ambulancias_tsu= leer_archivo()
problem = Problem()

todas_las_plazas = [(i, j) for i in range(1, dimension[0]+1) for j in range(1, dimension[1]+1)]

# Todo vehículo tiene que tener asignada una plaza y sólo una
for ambulancia in ambulancias:
    if ambulancia.split('-')[2] == 'C':  # Si el vehículo tiene congelador
        problem.addVariable(ambulancia, cargas)  # Solo puede ir a las plazas con conexión eléctrica

    else:
        problem.addVariable(ambulancia, todas_las_plazas)


#Dos vehículos distintos no pueden ocupar la misma plaza
problem.addConstraint(AllDifferentConstraint(), [variable for variable in ambulancias])
def restriccion_tsu_filas(a1, a2):
    if a1[0] == a2[0]:
        if a1[1] < a2[1]:
            return False
    return True
for a1 in ambulancias:
    if a1 in ambulancias_tsu:
        for a2 in ambulancias:
            if a1 != a2 and a2 not in ambulancias_tsu:
                problem.addConstraint(restriccion_tsu_filas, (a1, a2))

 # Por cuestiones de maniobrabilidad dentro del parking todo vehículo debe tener libre una plaza a izquierda o derecha (mirando en dirección a la salida).
def constraint_maniobrabilidad(a1, a2, a3):
    #Función que comprueba que todo vehículo debe tener libre una plaza a izquierda o derecha.
    if a1[1] == a2[1] == a3[1]:

        if (a1[0] == 1  and (a2[0] == a1[0] + 1 or a3[0] == a1[0] + 1)):
            return False
        
        elif (a1[0] == dimension[0] and (a2[0] == a1[0] - 1 or a3[0] == a1[0]-1)):
            return False
        
        elif (a1[0] == a2[0] + 1 and a1[0]== a3[0]- 1):
            return False
        
        elif (a1[0] == a2[0]- 1 and a1[0]== a3[0] + 1):
            return False
    return True
for a1 in ambulancias:
    for a2 in ambulancias:
        for a3 in ambulancias:
            if a1 != a2 != a3:
                problem.addConstraint(constraint_maniobrabilidad, (a1, a2, a3))

soluciones = problem.getSolutions()

num_soluciones = len(soluciones)
if num_soluciones == 0:
    print("No se ha encontrado soluciones.")
    exit()

# Llamar a la función guardar_soluciones con las soluciones obtenidas
guardar_soluciones(soluciones, dimension, ambulancias)
