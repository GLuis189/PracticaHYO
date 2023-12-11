import sys
import copy

# Estados [posicion ambulancia, energía, pasajeros, por recoger]
# Estados [(x,y), E, [C,C,C], [(x,y,N), (x,y,C)]]

lectura_mapa = sys.argv[1]
num_h = sys.argv[2]

# lectura_mapa = "parte-2/ASTAR-tests/mapa1.csv"

def leer_archivo():
    mapa = []
    with open(lectura_mapa, "r") as f:
        for linea in f:
            fila = linea.strip().split(";")
            for i, valor in enumerate(fila):
                if valor == '1' or valor == '2':
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
                estado[0] = (i,j)
    return estado


def cargar_salida():
    return

def ordenar_abrierta(nodos, costes):
    abierta = sorted(nodos, key=lambda nodo: costes[crear_tupla(nodo)])
    return abierta

def crear_tupla(lista):
    return tuple(tuple(i) if isinstance(i, list) else i for i in lista)

def arriba(estado):
    nuevo_estado = copy.deepcopy(estado)
    if nuevo_estado[0][0] == 0 or mapa[nuevo_estado[0][0] - 1][nuevo_estado[0][1]] == "X":
        return None, None
    nuevo_estado[0][0] -= 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        nuevo_estado[1] -= mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
        if nuevo_estado[1] == 0:
            return None, None
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        nuevo_estado[1] = 50
        return nuevo_estado, 1
    nuevo_estado[1] -= 1
    if nuevo_estado[1] == 0:
        return None, None
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        nuevo_estado[2].append("N")
        nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if estado[2].count("C") == 2:
            return nuevo_estado, 1
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
        return None, None
    nuevo_estado[0][0] += 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        nuevo_estado[1] -= mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
        if nuevo_estado[1] == 0:
            return None, None
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        nuevo_estado[1] = 50
        return nuevo_estado, 1
    nuevo_estado[1] -= 1
    if nuevo_estado[1] == 0:
        return None, None
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        nuevo_estado[2].append("N")
        nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if estado[2].count("C") == 2:
            return nuevo_estado, 1
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
        return None, None
    nuevo_estado[0][1] += 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        nuevo_estado[1] -= mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
        if nuevo_estado[1] == 0:
            return None, None
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        nuevo_estado[1] = 50
        return nuevo_estado, 1
    nuevo_estado[1] -= 1
    if nuevo_estado[1] == 0:
        return None, None
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        nuevo_estado[2].append("N")
        nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if estado[2].count("C") == 2:
            return nuevo_estado, 1
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
        return None, None
    nuevo_estado[0][1] -= 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        nuevo_estado[1] -= mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
        if nuevo_estado[1] == 0:
            return None, None
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        nuevo_estado[1] = 50
        return nuevo_estado, 1
    nuevo_estado[1] -= 1
    if nuevo_estado[1] == 0:
        return None, None
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[2]):
            return nuevo_estado, 1
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        nuevo_estado[2].append("N")
        nuevo_estado[3].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[2])>9:
            return nuevo_estado, 1
        if estado[2].count("C") == 2:
            return nuevo_estado, 1
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

            if s_arriba and s_arriba not in cerrada:
                if s_arriba not in abierta:
                    abierta.append(s_arriba)
                    coste[crear_tupla(s_arriba)] = coste[t_n] + c_arriba
                else:
                    if coste[crear_tupla(s_arriba)] > coste[t_n] + c_arriba:
                        coste[crear_tupla(s_arriba)] = coste[t_n] + c_arriba
            if s_abajo and s_abajo not in cerrada:
                if s_abajo not in abierta:
                    abierta.append(s_abajo)
                    coste[crear_tupla(s_abajo)] = coste[t_n] + c_abajo
                else:
                    if coste[crear_tupla(s_abajo)] > coste[t_n] + c_abajo:
                        coste[crear_tupla(s_abajo)] = coste[t_n] + c_abajo
            if s_derecha and s_derecha not in cerrada:
                if s_derecha not in abierta:
                    abierta.append(s_derecha)
                    coste[crear_tupla(s_derecha)] = coste[t_n] + c_derecha
                else:
                    if coste[crear_tupla(s_derecha)] > coste[t_n] + c_derecha:
                        coste[crear_tupla(s_derecha)] = coste[t_n] + c_derecha
            if s_izquierda and s_izquierda not in cerrada:
                if s_izquierda not in izquierda:
                    abierta.append(s_izquierda)
                    coste[crear_tupla(s_izquierda)] = coste[t_n] + c_izquierda
                else:
                    if coste[crear_tupla(s_izquierda)] > coste[t_n] + c_izquierda:
                        coste[crear_tupla(s_izquierda)] = coste[t_n] + c_izquierda
            abierta = ordenar_abrierta(abierta, coste)
            print("termine")
    print("termine")
   
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

a_estrella(inicial(), final())