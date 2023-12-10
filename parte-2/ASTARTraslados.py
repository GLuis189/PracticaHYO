import sys

lectura_mapa = sys.argv[1]
num_h = sys.argv[2]

def leer_archivo():
    mapa = []
    with open(lectura_mapa, "r") as f:
        for linea in f:
            fila = linea.strip().split(";")
            for i, valor in enumerate(fila):
                if valor == '1' or valor == '2':
                    fila[i] = int(valor)
            mapa.append(fila)
    return mapa

mapa = leer_archivo()

