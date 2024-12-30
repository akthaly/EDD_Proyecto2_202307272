from ..clientes_lista_circular_doble.Nodo import Nodo
from graphviz import Digraph

class ListaCircularDoblementeEnlazada:
    def __init__(self):
        self.head = None

    def insertar(self, cliente):
        nuevo_nodo = Nodo(cliente)
        if not self.head:

            self.head = nuevo_nodo
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
        else:
            actual = self.head
            while actual.siguiente != self.head and actual.cliente.getDPI() < cliente.getDPI():
                actual = actual.siguiente

            nuevo_nodo.siguiente = actual
            nuevo_nodo.anterior = actual.anterior
            actual.anterior.siguiente = nuevo_nodo
            actual.anterior = nuevo_nodo

            if actual == self.head and cliente.getDPI() < self.head.cliente.getDPI():
                self.head = nuevo_nodo

    def imprimir(self):
        if self.head is None:
            print("La lista está vacía.")
            return

        actual = self.head
        while True:
            print(f"DPI: {actual.cliente.getDPI()} Nombre: {actual.cliente.getNombre()} {actual.cliente.getApellido()}")
            actual = actual.siguiente
            if actual == self.head:
                break

    def buscar(self, dpi):
        if self.head is None:
            return None

        actual = self.head
        while True:
            if actual.cliente.getDPI() == dpi:
                return actual.cliente
            actual = actual.siguiente
            if actual == self.head:
                break

        return None
    
    def eliminar_cliente_por_dpi(self, dpi):
        if self.head is None:  
            return False
        
        actual = self.head
        while True:
            if actual.cliente.getDPI() == dpi:
                
                if actual.siguiente == actual:
                    self.head = None
                    return True

                else:
                    anterior = actual.anterior
                    siguiente = actual.siguiente
                    anterior.siguiente = siguiente
                    siguiente.anterior = anterior

                    if actual == self.head:
                        self.head = actual.siguiente

                return True

            actual = actual.siguiente
            if actual == self.head:
                break

        return False  # if the client was not found



    def estructura_cliente_graphviz(lista):
        if not lista.head:
            print("La lista está vacía. No se puede generar el gráfico.")
            return

        grafo = Digraph(format='svg')
        grafo.attr(rankdir='LR', size='8')

        actual = lista.head
        nodo_inicial = id(actual)

        while True:
            nodo_id = str(id(actual))
            label = f"DPI: {actual.cliente.dpi} \\nNombre: {actual.cliente.nombre} {actual.cliente.apellido}"
            grafo.node(nodo_id, label, shape="record")

            if actual.siguiente:
                siguiente_id = str(id(actual.siguiente))
                grafo.edge(nodo_id, siguiente_id, label="siguiente", dir="forward")

            if actual.anterior:
                anterior_id = str(id(actual.anterior))
                grafo.edge(anterior_id, nodo_id, label="anterior", dir="back")

            actual = actual.siguiente

            if id(actual) == nodo_inicial:
                break

        grafo.attr(overlap='false', splines='true')

        grafo.render("Estructura_Clientes", cleanup=True)
        print(f"Imagen generada: Estructura_Clientes.svg")