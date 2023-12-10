a = [1,2,3,4,5]
s = {1: 0, 2: 2, 3: 1, 4: 0, 5: 0}

def ordenar_nodos_por_coste(nodos, costes):
    nodos_ordenados = sorted(nodos, key=lambda nodo: costes[nodo])
    return nodos_ordenados

print(ordenar_nodos_por_coste(a, s))