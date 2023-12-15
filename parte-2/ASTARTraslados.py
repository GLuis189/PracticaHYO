import sys
import copy
import datetime
import heapq

# Estados [posicion ambulancia, energía, pasajeros, por recoger]
# Estados [(x,y), [C,C,C], [(x,y,N), (x,y,C)]]

lectura_mapa = sys.argv[1]
num_h = sys.argv[2]
if num_h not in ["1", "2"]:
    exit()
salida = lectura_mapa[:-3] + "output"
stats = lectura_mapa[:-4] + "-" + str(num_h) + ".stat"

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

def obtener_destinos():
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "CC":
                cc = (i,j)
            if mapa[i][j] == "CN":
                cn = (i,j)
            if mapa[i][j] == "P":
                p = (i,j)    
    return cc, cn, p

def inicial():
    estado = [None,[],[]]
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "P":
                estado[0] = [i,j]
            if mapa[i][j] == "C":
                estado[2].append((i,j,"C"))
            if mapa[i][j] == "N":
                estado[2].append((i,j,"N"))
    return estado

def final():
    estado = [None, [], []]
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "P":
                estado[0] = [i,j]
    return estado

def crear_tupla(lista):
    return tuple(tuple(i) if isinstance(i, list) else i for i in lista)

def guardar_solucion(camino, mapa, gasolina):
    with open(salida, "w", newline='') as f:
        for nodo in camino:
            f.write("({},{}):{}:{}\n".format(nodo[0][0], nodo[0][1], mapa[nodo[0][0]][nodo[0][1]], gasolina[crear_tupla(nodo)]))

def guardar_stats(camino, fin, coste_total, cerrada):
    with open(stats, "w", newline='') as f:
        f.write("Tiempo total: {}\n".format(despues - antes))
        f.write("Coste total: {}\n".format(coste_total[crear_tupla(fin)]))
        f.write("Longitud del plan: {}\n".format(len(camino)))
        f.write("Nodos expandidos: {}\n".format(len(cerrada)))

def arriba(estado):
    nuevo_estado = copy.deepcopy(estado)
    if nuevo_estado[0][0] == 0 or mapa[nuevo_estado[0][0] - 1][nuevo_estado[0][1]] == "X":
        return 0, 0
    nuevo_estado[0][0] -= 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[1]):
            return nuevo_estado, 1
        if len(nuevo_estado[1])>9:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "N") for pasajero in nuevo_estado[2]):
            nuevo_estado[1].append("N")
            nuevo_estado[2].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[1])>9:
            return nuevo_estado, 1
        if nuevo_estado[1].count("C") == 2:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "C") for pasajero in nuevo_estado[2]):
            nuevo_estado[1].append("C")
            nuevo_estado[2].remove((nuevo_estado[0][0], nuevo_estado[0][1], "C"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in nuevo_estado[1]):
            return nuevo_estado, 1
        nuevo_estado[1] = []
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CC":
        while "C" in nuevo_estado[1]:
            nuevo_estado[1].remove("C")
        return nuevo_estado, 1
    
def abajo(estado):
    nuevo_estado = copy.deepcopy(estado)
    if nuevo_estado[0][0] == filas -1 or mapa[nuevo_estado[0][0] + 1][nuevo_estado[0][1]] == "X":
        return 0, 0
    nuevo_estado[0][0] += 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[1]):
            return nuevo_estado, 1
        if len(nuevo_estado[1])>9:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "N") for pasajero in nuevo_estado[2]):
            nuevo_estado[1].append("N")
            nuevo_estado[2].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[1])>9:
            return nuevo_estado, 1
        if nuevo_estado[1].count("C") == 2:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "C") for pasajero in nuevo_estado[2]):
            nuevo_estado[1].append("C")
            nuevo_estado[2].remove((nuevo_estado[0][0], nuevo_estado[0][1], "C"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in nuevo_estado[1]):
            return nuevo_estado, 1
        nuevo_estado[1] = []
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CC":
        while "C" in nuevo_estado[1]:
            nuevo_estado[1].remove("C")
        return nuevo_estado, 1

def derecha(estado):
    nuevo_estado = copy.deepcopy(estado)
    if nuevo_estado[0][1] == columnas -1 or mapa[nuevo_estado[0][0]][nuevo_estado[0][1] +1] == "X":
        return 0, 0
    nuevo_estado[0][1] += 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[1]):
            return nuevo_estado, 1
        if len(nuevo_estado[1])>9:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "N") for pasajero in nuevo_estado[2]):
            nuevo_estado[1].append("N")
            nuevo_estado[2].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[1])>9:
            return nuevo_estado, 1
        if nuevo_estado[1].count("C") == 2:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "C") for pasajero in nuevo_estado[2]):
            nuevo_estado[1].append("C")
            nuevo_estado[2].remove((nuevo_estado[0][0], nuevo_estado[0][1], "C"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in nuevo_estado[1]):
            return nuevo_estado, 1
        nuevo_estado[1] = []
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CC":
        while "C" in nuevo_estado[1]:
            nuevo_estado[1].remove("C")
        return nuevo_estado, 1

def izquierda(estado):
    nuevo_estado = copy.deepcopy(estado)
    if nuevo_estado[0][1] ==0 or mapa[nuevo_estado[0][0]][nuevo_estado[0][1] - 1] == "X":
        return 0, 0
    nuevo_estado[0][1] -= 1
    if isinstance(mapa[nuevo_estado[0][0]][nuevo_estado[0][1]], int):
        return nuevo_estado , mapa[nuevo_estado[0][0]][nuevo_estado[0][1]]
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "P":
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "N":
        if any(pasajero == "C" for pasajero in nuevo_estado[1]):
            return nuevo_estado, 1
        if len(nuevo_estado[1])>9:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "N") for pasajero in nuevo_estado[2]):
            nuevo_estado[1].append("N")
            nuevo_estado[2].remove((nuevo_estado[0][0], nuevo_estado[0][1], "N"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "C":
        if len(nuevo_estado[1])>9:
            return nuevo_estado, 1
        if nuevo_estado[1].count("C") == 2:
            return nuevo_estado, 1
        if any(pasajero == (nuevo_estado[0][0], nuevo_estado[0][1], "C") for pasajero in nuevo_estado[2]):
            nuevo_estado[1].append("C")
            nuevo_estado[2].remove((nuevo_estado[0][0], nuevo_estado[0][1], "C"))
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CN":
        if any(pasajero == "C" for pasajero in nuevo_estado[1]):
            return nuevo_estado, 1
        nuevo_estado[1] = []
        return nuevo_estado, 1
    if mapa[nuevo_estado[0][0]][nuevo_estado[0][1]] == "CC":
        while "C" in nuevo_estado[1]:
            nuevo_estado[1].remove("C")
        return nuevo_estado, 1
    

def heuristica(estado):
    if num_h == "1":
        punto1 = estado[0]
        distancia_min = 99999
        if len(estado[1]) < 10 and estado[2] != []:
            # Recoger al pasajero mas cercano
            for punto in estado[2]:
                punto2 = (punto[0],punto[1])
                distancia = abs(punto1[0] - punto2[0]) + abs(punto1[1] - punto2[1])
                if distancia < distancia_min:
                        distancia_min = distancia
            return distancia_min
        if estado[1] == [] and estado[2] == []:
            punto2 = p
            return abs(punto1[0] - punto2[0]) + abs(punto1[1] - punto2[1])
        if estado[1][-1] == "C":
            punto2 = cc
            return abs(punto1[0] - punto2[0]) + abs(punto1[1] - punto2[1])
        if estado[1][-1] == "N":
            punto2 = cn
            return abs(punto1[0] - punto2[0]) + abs(punto1[1] - punto2[1])
        return 0
    if num_h == "2":
        # Heurística
        return len(estado[2])
    return

def a_estrella(inicio, fin):
    abierta = []
    heapq.heappush(abierta, (heuristica(inicio), inicio))
    cerrada = set()
    exito = False
    camino = {}
    gasolina = {crear_tupla(inicio): 50}
    coste_total= {crear_tupla(inicio): 0}
    coste = {crear_tupla(inicio): heuristica(inicio)} 

    while abierta and not exito: 
        _, n = heapq.heappop(abierta)
        cerrada.add(crear_tupla(n))

        if n == fin:
            exito = True
        else:
            t_n = crear_tupla(n)
            s_arriba, c_arriba = arriba(n)
            s_abajo, c_abajo = abajo(n)
            s_derecha, c_derecha = derecha(n)
            s_izquierda, c_izquierda = izquierda(n)

            for s, c_s in [(s_arriba, c_arriba), (s_abajo, c_abajo), (s_derecha, c_derecha), (s_izquierda, c_izquierda)]:
                #print(c_s)
                if s != 0 and crear_tupla(s) not in cerrada:
                    h_s = heuristica(s)
                    t_s = crear_tupla(s)
                    if s not in (n for _, n in abierta) or coste[t_s] > coste[t_n] + c_s + h_s:
                        #nuevo
                        if mapa[s[0][0]][s[0][1]] == 'P':
                            gasolina_nuevo = 50
                        else:
                            gasolina_nuevo = gasolina[t_n] - c_s
                        if gasolina_nuevo>0:
                        #nuevo
                            coste_total[t_s] = coste_total[t_n] + c_s
                            coste[t_s] = coste[t_n] + c_s + h_s
                            camino[t_s] = n
                            #nuevo
                            gasolina[t_s]= gasolina_nuevo
                            heapq.heappush(abierta, (coste[t_s], s))
    
    if exito:
        # Si se encontró un camino, reconstruirlo a partir del diccionario 'camino'
        camino_final = [fin]
        estado_actual = crear_tupla(fin)
        while estado_actual != crear_tupla(inicio):
            padre  = camino[estado_actual]
            camino_final.append(padre)
            estado_actual = crear_tupla(padre)
        camino_final.reverse()  # Invertir el camino para que vaya desde el inicio hasta el fin
        return camino_final, coste, gasolina, cerrada, coste_total
    return 0, 0, 0, 0, 0


antes = datetime.datetime.now()
mapa, filas, columnas = leer_archivo()
cc, cn, p = obtener_destinos()
inicio = inicial()
fin = final()
camino, coste, gasolina, cerrada, coste_total = a_estrella(inicio, fin)
despues = datetime.datetime.now()
#imprimir_solucion(camino, mapa, coste, fin)
if camino == 0:
    with open(salida, "w", newline='') as f:
        f.write("No se ha encontrado solucion")
        exit()
guardar_solucion(camino, mapa, gasolina)
guardar_stats(camino, fin, coste_total, cerrada)
print("Tiempo: ", despues -antes)

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
