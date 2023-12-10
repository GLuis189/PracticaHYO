import sys

lectura_mapa = sys.argv[1]
num_h = sys.argv[2]
# Estados [posicion ambulancia, energía, pasajeros, por recoger]
# Estados [(x,y), E, [C,C,C], [(x,y,N), (x,y,C)]]
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
    abierta = sorted(nodos, key=lambda nodo: costes[nodo])
    return abierta

def arriba(estado):
    if estado[0][0] == filas - 1 or mapa[estado[0][0] + 1][estado[0][1]] == "X":
        return None, None
    estado[0][0] += 1
    if isinstance(mapa[estado[0][0]][estado[0][1]], int):
        estado[1] -= mapa[estado[0][0]][estado[0][1]]
        if estado[1] == 0:
            return None, None
        return estado , mapa[estado[0][0]][estado[0][1]]
    if mapa[estado[0][0]][estado[0][1]] == "P":
        estado[1] = 50
        return estado , mapa[estado[0][0]][estado[0][1]]
    estado[1] -= 1
    if estado[1] == 0:
        return None, None
    if mapa[estado[0][0]][estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in estado[2]):
            return estado , 1
        if len(estado[2])>9:
            return estado , 1
        estado[2].append("N")
        estado[3].remove((estado[0][0], estado[0][1], "N"))
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "C":
        if len(estado[2])>9:
            return estado , 1
        if estado[2].count("C") == 2:
            return estado , 1
        estado[2].append("C")
        estado[3].remove((estado[0][0], estado[0][1], "C"))
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in estado[2]):
            return estado , 1
        estado[2] = []
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "CC":
        while "C" in estado[2]:
            estado[2].remove("C")
        return estado , 1
    
def abajo(estado):
    if estado[0][0] == 0 or mapa[estado[0][0] - 1][estado[0][1]] == "X":
        return None, None
    estado[0][0] -= 1
    if isinstance(mapa[estado[0][0]][estado[0][1]], int):
        estado[1] -= mapa[estado[0][0]][estado[0][1]]
        if estado[1] == 0:
            return None, None
        return estado , mapa[estado[0][0]][estado[0][1]]
    if mapa[estado[0][0]][estado[0][1]] == "P":
        estado[1] = 50
        return estado , mapa[estado[0][0]][estado[0][1]]
    estado[1] -= 1
    if estado[1] == 0:
        return None, None
    if mapa[estado[0][0]][estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in estado[2]):
            return estado , 1
        if len(estado[2])>9:
            return estado , 1
        estado[2].append("N")
        estado[3].remove((estado[0][0], estado[0][1], "N"))
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "C":
        if len(estado[2])>9:
            return estado , 1
        if estado[2].count("C") == 2:
            return estado , 1
        estado[2].append("C")
        estado[3].remove((estado[0][0], estado[0][1], "C"))
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in estado[2]):
            return estado , 1
        estado[2] = []
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "CC":
        while "C" in estado[2]:
            estado[2].remove("C")
        return estado , 1

def derecha(estado):
    if estado[0][1] == columnas - 1 or mapa[estado[0][0]][estado[0][1] + 1] == "X":
        return None, None
    estado[0][1] += 1
    if isinstance(mapa[estado[0][0]][estado[0][1]], int):
        estado[1] -= mapa[estado[0][0]][estado[0][1]]
        if estado[1] == 0:
            return None, None
        return estado , mapa[estado[0][0]][estado[0][1]]
    if mapa[estado[0][0]][estado[0][1]] == "P":
        estado[1] = 50
        return estado , mapa[estado[0][0]][estado[0][1]]
    estado[1] -= 1
    if estado[1] == 0:
        return None, None
    if mapa[estado[0][0]][estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in estado[2]):
            return estado , 1
        if len(estado[2])>9:
            return estado , 1
        estado[2].append("N")
        estado[3].remove((estado[0][0], estado[0][1], "N"))
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "C":
        if len(estado[2])>9:
            return estado , 1
        if estado[2].count("C") == 2:
            return estado , 1
        estado[2].append("C")
        estado[3].remove((estado[0][0], estado[0][1], "C"))
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in estado[2]):
            return estado , 1
        estado[2] = []
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "CC":
        while "C" in estado[2]:
            estado[2].remove("C")
        return estado , 1

def izquierda(estado):
    if estado[0][1] == 0 or mapa[estado[0][0]][estado[0][1] - 1] == "X":
        return None, None
    estado[0][1] -= 1
    if isinstance(mapa[estado[0][0]][estado[0][1]], int):
        estado[1] -= mapa[estado[0][0]][estado[0][1]]
        if estado[1] == 0:
            return None, None
        return estado , mapa[estado[0][0]][estado[0][1]]
    if mapa[estado[0][0]][estado[0][1]] == "P":
        estado[1] = 50
        return estado , mapa[estado[0][0]][estado[0][1]]
    estado[1] -= 1
    if estado[1] == 0:
        return None, None
    if mapa[estado[0][0]][estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in estado[2]):
            return estado , 1
        if len(estado[2])>9:
            return estado , 1
        estado[2].append("N")
        estado[3].remove((estado[0][0], estado[0][1], "N"))
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "C":
        if len(estado[2])>9:
            return estado , 1
        if estado[2].count("C") == 2:
            return estado , 1
        estado[2].append("C")
        estado[3].remove((estado[0][0], estado[0][1], "C"))
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in estado[2]):
            return estado , 1
        estado[2] = []
        return estado , 1
    if mapa[estado[0][0]][estado[0][1]] == "CC":
        while "C" in estado[2]:
            estado[2].remove("C")
        return estado , 1
    
def a_estrella(inical, final):
    abierta = [inical]
    cerrada = []
    exito = False
    camino = {}
    coste = {inicial : 0}
    while abierta != [] and not exito:
        n = abierta.pop(0)
        cerrada.append(n)
        if n == final:
            exito = True
        else:
            s_arriba, c_arriba = arriba(n)
            s_abajo, c_abajo = abajo(n)
            s_derecha, c_derecha = derecha(n)
            s_izquierda, c_izquierda = izquierda(n)
            print(s_abajo,s_arriba,s_derecha,s_izquierda)
            if s_arriba and s_arriba not in cerrada:
                if s_arriba not in abierta:
                    abierta.append(s_arriba)
                    coste[s_arriba] = coste[n] + c_arriba
                else:
                    if coste[s_arriba] > coste[n] + c_arriba:
                        coste[s_arriba] = coste[n] + c_arriba
            if s_abajo and s_abajo not in cerrada:
                if s_abajo not in abierta:
                    abierta.append(s_abajo)
                    coste[s_abajo] = coste[n] + c_abajo
                else:
                    if coste[s_abajo] > coste[n] + c_abajo:
                        coste[s_abajo] = coste[n] + c_abajo
            if s_derecha and s_derecha not in cerrada:
                if s_derecha not in abierta:
                    abierta.append(s_derecha)
                    coste[s_derecha] = coste[n] + c_derecha
                else:
                    if coste[s_derecha] > coste[n] + c_derecha:
                        coste[s_derecha] = coste[n] + c_derecha
            if s_izquierda and s_izquierda not in cerrada:
                if s_izquierda not in izquierda:
                    abierta.append(s_izquierda)
                    coste[s_izquierda] = coste[n] + c_izquierda
                else:
                    if coste[s_izquierda] > coste[n] + c_izquierda:
                        coste[s_izquierda] = coste[n] + c_izquierda
            abierta = ordenar_abrierta(abierta, coste)
            print("termine")
    print("termine")
   
    return

mapa, filas, columnas = leer_archivo()
a_estrella(inicial(), final())

