import heapq
from graphviz import Graph 

class GrafoRutas:
    def __init__(self):
        self.grafo = {}

    def agregar_ruta(self, origen, destino, tiempo):

        if origen not in self.grafo:
            self.grafo[origen] = []

        if destino not in self.grafo:
            self.grafo[destino] = []

        if not any(dest == destino for dest, _ in self.grafo[origen]):
            self.grafo[origen].append((destino, tiempo))
        if not any(orig == origen for orig, _ in self.grafo[destino]):
            self.grafo[destino].append((origen, tiempo))

    def mostrar_grafo(self):
        for lugar, rutas in self.grafo.items():
            print(f"{lugar}: {rutas}")

    def obtener_vecinos(self, lugar):
        return self.grafo.get(lugar, [])

    def generar_grafo_graphviz(self, nombre_archivo="grafo_rutas"):

        grafo = Graph("GrafoRutas", format="png")

        aristas_agregadas = set()

        for origen, destinos in self.grafo.items():
            for destino, tiempo in destinos:

                if (origen, destino) not in aristas_agregadas and (destino, origen) not in aristas_agregadas:
                    grafo.edge(origen, destino, label=str(tiempo))
                    aristas_agregadas.add((origen, destino))

        grafo.render(nombre_archivo, view=True)
        print(f"Grafo generado y guardado como {nombre_archivo}.png")

    def calcular_mejor_ruta(self, origen, destino):
        if origen not in self.grafo or destino not in self.grafo:
            raise ValueError("El origen o destino no existen en el grafo.")

        # Diccionario para almacenar el menor costo a cada nodo
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[origen] = 0

        # Para rastrear los predecesores en el camino más corto
        predecesores = {nodo: None for nodo in self.grafo}

        # Cola de prioridad para explorar los nodos
        cola = [(0, origen)]  # (distancia acumulada, nodo)

        while cola:
            distancia_actual, nodo_actual = heapq.heappop(cola)

            if nodo_actual == destino:
                break

            for vecino, peso in self.grafo[nodo_actual]:
                nueva_distancia = distancia_actual + peso

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola, (nueva_distancia, vecino))

        # Reconstruir el camino más corto
        camino = []
        nodo_actual = destino
        while nodo_actual is not None:
            camino.insert(0, nodo_actual)
            nodo_actual = predecesores[nodo_actual]

        if distancias[destino] == float('inf'):
            raise ValueError("No existe una ruta entre el origen y el destino.")

        return camino, distancias[destino]


# grafo_rutas = GrafoRutas()

# rutas = [
#     ("Oviedo", "Bilbao", 304),
#     ("Bilbao", "Zaragoza", 324),
#     ("Bilbao", "Madrid", 395),
#     ("Bilbao", "Valladolid", 280),
#     ("Zaragoza", "Barcelona", 296),
#     ("Barcelona", "Gerona", 100),
#     ("Zaragoza", "Madrid", 325)
# ]

# for origen, destino, tiempo in rutas:
#     grafo_rutas.agregar_ruta(origen, destino, tiempo)

# grafo_rutas.mostrar_grafo()

# grafo_rutas.generar_grafo_graphviz()
