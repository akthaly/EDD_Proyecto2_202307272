from Clases.Viajes import Viaje
from Estructuras.viajes_lista_simple.ListaSimple import ListaSimple


class GestorViajes:
    def __init__(self, lista_clientes, arbol_vehiculos, grafo_rutas):
        self.lista_clientes = lista_clientes  # Lista circular doblemente enlazada
        self.arbol_vehiculos = arbol_vehiculos  # Árbol B
        self.grafo_rutas = grafo_rutas  # Grafo de rutas
        self.viajes = []  # Lista de viajes registrados
        self.contador_id = 0  # Contador para IDs únicos de viajes

    def crear_viaje(self, dpi_cliente, placa_vehiculo, origen, destino, fecha_hora_inicio):
        # Buscar cliente
        cliente = self.lista_clientes.buscar(dpi_cliente)
        if not cliente:
            raise ValueError(f"Cliente con DPI {dpi_cliente} no encontrado.")

        # Buscar vehículo
        vehiculo = self.arbol_vehiculos.buscar_vehiculo(placa_vehiculo)
        if not vehiculo:
            raise ValueError(f"Vehículo con placa {placa_vehiculo} no encontrado.")

        # Calcular la mejor ruta
        camino, tiempo_total = self.grafo_rutas.calcular_mejor_ruta(origen, destino)

        # Crear la lista simple de la ruta
        ruta = ListaSimple()
        tiempo_acumulado = 0
        for i in range(len(camino) - 1):
            origen = camino[i]
            destino = camino[i + 1]
            tiempo = next(t for d, t in self.grafo_rutas.obtener_vecinos(origen) if d == destino)
            tiempo_acumulado += tiempo
            ruta.agregar(f"{origen} -> {destino} ({tiempo_acumulado}s)")

        # Asignar un ID único al viaje
        self.contador_id += 1
        viaje_id = self.contador_id

        # Registrar el viaje
        viaje = Viaje(cliente, vehiculo, ruta, fecha_hora_inicio, viaje_id)
        self.viajes.append(viaje)
        print(f"Viaje creado exitosamente: {viaje.getRuta()}")

    def obtener_ruta_por_id(self, viaje_id):
        # Buscar el viaje por su ID
        for viaje in self.viajes:
            if viaje.get_id() == viaje_id:
                return viaje.__str__()
        raise ValueError(f"No se encontró un viaje con ID {viaje_id}.")
