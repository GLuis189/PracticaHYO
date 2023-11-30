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
    #print(dimension)

    # La segunda es la disposición de estaciones de carga 
    # Es una lista con tuplas (fila, columna) que indica la posicion de esta
    partes = parking[1][3:].split(')(')
    partes[0] = partes[0][1:]
    partes[-1] = partes[-1][:-1]
    cargas = [tuple(map(int, parte.split(','))) for parte in partes]
    #print(cargas)

    # El resto son ambulancias
    # Es una lista con tuplas de la siguiente manera (ID, TSU/TNU, C/X) ID como entero?
    ambulancias = [(int(partes[0]), partes[1], partes[2]) for partes in (elemento.split('-') for elemento in parking[2:])]
    #print(abmulancias)

    return dimension, cargas, ambulancias



dimension, cargas, ambulancias = leer_archivo()

problem = Problem()
for i in range(dimension[0]):
    for j in range(dimension[1]):
        problem.addVariable("X{}{}".format(i,j), list(range(len(ambulancias) + 1))[1:] + ["-"])

