import sys
import copy

# Estados [posicion ambulancia, energía, pasajeros, por recoger]
# Estados [(x,y), E, [C,C,C], [(x,y,N), (x,y,C)]]

lectura_mapa = sys.argv[1]
num_h = sys.argv[2]
salida = lectura_mapa[:-3] + "output"

# lectura_mapa = "parte-2/ASTAR-tests/mapa1.csv"

def leer_archivo():
    mapa = []
    with open(lectura_mapa, "r") as f:
        for linea in f:
            fila = linea.strip().split(";")
            for i, valor in enumerate(fila):
                if valor.isdigit():
                    fila[i] = int(valor)
            mapa.append(fila)
    return mapa, len(mapa), len(mapa[0])

def inicial():
    estado = [None, 50, [],[]]
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "P":
                estado[0] = [i,j]
            if mapa[i][j] == "C":
                estado[3].append((i,j,"C"))
            if mapa[i][j] == "N":
                estado[3].append((i,j,"N"))
    return estado

def final():
    estado = [None, 50, [], []]
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "P":
                estado[0] = [i,j]
    return estado

def ordenar_abrierta(nodos, costes):
    abierta = sorted(nodos, key=lambda nodo: costes[crear_tupla(nodo)])
    return abierta

def crear_tupla(lista):
    return tuple(tuple(i) if isinstance(i, list) else i for i in lista)

def imprimir_solucion(camino, mapa, coste, fin):
    # coste = coste[fin]
    for nodo in camino:
        print("({},{}):{}:{}".format(nodo[0][0], nodo[0][1], mapa[nodo[0][0]][nodo[0][1]], nodo[1]))

def guardar_solucion(camino, mapa, coste, fin):
    with open(salida, "w", newline='') as f:
        for nodo in camino:
            f.write("({},{}):{}:{}\n".format(nodo[0][0], nodo[0][1], mapa[nodo[0][0]][nodo[0][1]], nodo[1]))


def arriba(estado):
    nuevo_estado = copy.deepcopy(estado)
    if nuevo_estado[0][0] == 0 or mapa[nuevo_estado[0][0] - 1][nuevo_estado[0][1]] == "X":
        return 0, 0
    nuevo_estado[0][0] -= 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        nuevo_estado[1] -= mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
        if nuevo_estado[1] == 0:
            return 0, 0
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        nuevo_estado[1] = 50
        return nuevo_estado, 1
    nuevo_estado[1] -= 1
    if nuevo_estado[1] == 0:
        return 0, 0
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "N") for pasajero in nuevo_estado[3]):
            nuevo_estado[2].append("N")
            nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if nuevo_estado[2].count("C") == 2:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "C") for pasajero in nuevo_estado[3]):
            nuevo_estado[2].append("C")
            nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "C"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        nuevo_estado[2] = []
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CC":
        while "C" in nuevo_estado[2]:
            nuevo_estado[2].remove("C")
        return nuevo_estado, 1
    
def abajo(estado):
    nuevo_estado = copy.deepcopy(estado)
    if nuevo_estado[0][0] == filas - 1 or mapa[nuevo_estado[0][0] + 1][nuevo_estado[0][1]] == "X":
        return 0, 0
    nuevo_estado[0][0] += 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        nuevo_estado[1] -= mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
        if nuevo_estado[1] == 0:
            return 0, 0 
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        nuevo_estado[1] = 50
        return nuevo_estado, 1
    nuevo_estado[1] -= 1
    if nuevo_estado[1] == 0:
        return 0, 0
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "N") for pasajero in nuevo_estado[3]):
            nuevo_estado[2].append("N")
            nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if nuevo_estado[2].count("C") == 2:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "C") for pasajero in nuevo_estado[3]):
            nuevo_estado[2].append("C")
            nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "C"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        nuevo_estado[2] = []
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CC":
        while "C" in nuevo_estado[2]:
            nuevo_estado[2].remove("C")
        return nuevo_estado, 1

def derecha(estado):
    nuevo_estado = copy.deepcopy(estado)
    if nuevo_estado[0][1] == columnas - 1 or mapa[nuevo_estado[0][0]][nuevo_estado[0][1] + 1] == "X":
        return 0, 0
    nuevo_estado[0][1] += 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        nuevo_estado[1] -= mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
        if nuevo_estado[1] == 0:
            return 0, 0
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        nuevo_estado[1] = 50
        return nuevo_estado, 1
    nuevo_estado[1] -= 1
    if nuevo_estado[1] == 0:
        return 0, 0
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "N") for pasajero in nuevo_estado[3]):
            nuevo_estado[2].append("N")
            nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if nuevo_estado[2].count("C") == 2:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "C") for pasajero in nuevo_estado[3]):
            nuevo_estado[2].append("C")
            nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "C"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        nuevo_estado[2] = []
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CC":
        while "C" in nuevo_estado[2]:
            nuevo_estado[2].remove("C")
        return nuevo_estado, 1

def izquierda(estado):
    nuevo_estado = copy.deepcopy(estado)
    if nuevo_estado[0][1] == 0 or mapa[nuevo_estado[0][0]][nuevo_estado[0][1] - 1] == "X":
        return 0, 0
    nuevo_estado[0][1] -= 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        nuevo_estado[1] -= mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
        if nuevo_estado[1] == 0:
            return 0, 0
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        nuevo_estado[1] = 50
        return nuevo_estado, 1
    nuevo_estado[1] -= 1
    if nuevo_estado[1] == 0:
        return 0, 0
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "N") for pasajero in nuevo_estado[3]):
            nuevo_estado[2].append("N")
            nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if nuevo_estado[2].count("C") == 2:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "C") for pasajero in nuevo_estado[3]):
            nuevo_estado[2].append("C")
            nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "C"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        nuevo_estado[2] = []
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CC":
        while "C" in nuevo_estado[2]:
            nuevo_estado[2].remove("C")
        return nuevo_estado, 1
    
def a_estrella(inicio, fin):
    abierta = [inicio]
    cerrada = []
    exito = False
    camino = {}
    coste = {crear_tupla(inicio): 0} 
    while abierta != [] and not exito:
        n = abierta.pop(0)
        cerrada.append(n)
        if n == fin:
            exito = True
        else:
            t_n = crear_tupla(n)
            s_arriba, c_arriba = arriba(n)
            s_abajo, c_abajo = abajo(n)
            s_derecha, c_derecha = derecha(n)
            s_izquierda, c_izquierda = izquierda(n)

            if s_arriba != 0 and s_arriba not in cerrada:
                if s_arriba not in abierta:
                    abierta.append(s_arriba)
                    coste[crear_tupla(s_arriba)] = coste[t_n] + c_arriba
                    camino[crear_tupla(s_arriba)] = n
                else:
                    if coste[crear_tupla(s_arriba)] > coste[t_n] + c_arriba:
                        coste[crear_tupla(s_arriba)] = coste[t_n] + c_arriba
                        camino[crear_tupla(s_arriba)] = n
            if s_abajo != 0 and s_abajo not in cerrada:
                if s_abajo not in abierta:
                    abierta.append(s_abajo)
                    coste[crear_tupla(s_abajo)] = coste[t_n] + c_abajo
                    camino[crear_tupla(s_abajo)] = n
                else:
                    if coste[crear_tupla(s_abajo)] > coste[t_n] + c_abajo:
                        coste[crear_tupla(s_abajo)] = coste[t_n] + c_abajo
                        camino[crear_tupla(s_abajo)] = n
            if s_derecha != 0 and s_derecha not in cerrada:
                if s_derecha not in abierta:
                    abierta.append(s_derecha)
                    coste[crear_tupla(s_derecha)] = coste[t_n] + c_derecha
                    camino[crear_tupla(s_derecha)] = n
                else:
                    if coste[crear_tupla(s_derecha)] > coste[t_n] + c_derecha:
                        coste[crear_tupla(s_derecha)] = coste[t_n] + c_derecha
                        camino[crear_tupla(s_derecha)] = n
            if s_izquierda != 0 and s_izquierda not in cerrada:
                if s_izquierda not in abierta:
                    abierta.append(s_izquierda)
                    coste[crear_tupla(s_izquierda)] = coste[t_n] + c_izquierda
                    camino[crear_tupla(s_izquierda)] = n
                else:
                    if coste[crear_tupla(s_izquierda)] > coste[t_n] + c_izquierda:
                        coste[crear_tupla(s_izquierda)] = coste[t_n] + c_izquierda
                        camino[crear_tupla(s_izquierda)] = n
            abierta = ordenar_abrierta(abierta, coste)
    if exito:
        # Si se encontró un camino, reconstruirlo a partir del diccionario 'camino'
        camino_final = [fin]
        estado_actual = crear_tupla(fin)
        while estado_actual != crear_tupla(inicio):
            padre  = camino[estado_actual]
            camino_final.append(padre)
            estado_actual = crear_tupla(padre)
        camino_final.reverse()  # Invertir el camino para que vaya desde el inicio hasta el fin
        return camino_final, coste
    return

mapa, filas, columnas = leer_archivo()

# inicio = inicial()
# print("Inicio {}".format(inicio))
# arriba_estado, coste_arriba = arriba(inicio)
# print("Arriba {} coste {}".format(arriba, coste_arriba))
# abajo_estado, coste_abajo = abajo(inicio)
# print("Abajo {} coste {}".format(abajo_estado, coste_abajo))
# derecha_estado, coste_derecha = derecha(inicio)
# print("Derecha {} coste {}".format(derecha_estado, coste_derecha))
# izquierda_estado, coste_izquierda = izquierda(inicio)
# print("Izquierda {} coste {}".format(izquierda_estado, coste_izquierda))
# derecha_abajo, coste_derecha_abajo = abajo(derecha_estado)
# print("Derecha {} coste {}".format(derecha_abajo, coste_derecha_abajo + coste_derecha))
# print("Derecha {} coste {}".format(derecha_estado, coste_derecha))

inicio = inicial()
fin = final()
camino, coste = a_estrella(inicio, fin)
imprimir_solucion(camino, mapa, coste, fin)
guardar_solucion(camino, mapa, coste, fin)