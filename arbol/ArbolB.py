from graphviz import Digraph

from Clases.Vehiculos import Vehiculo

class Nodo:
    def __init__(self, es_hoja: bool = False):
        self.es_hoja : bool = es_hoja   
        self.llave : list[int] = [] 
        self.hijo : list[Nodo] = []

class ArbolB:
    def __init__(self, orden : int):
        self.raizPricipal: Nodo = Nodo(True)    
        self.orden: int = orden


    def insertar_vehiculo(self, vehiculo: Vehiculo):
        raiz: Nodo = self.raizPricipal

        self.insertar_nodo_vacio(raiz, vehiculo)

        if len(raiz.llave) > self.orden - 1:
            nodo: Nodo = Nodo()
            self.raizPricipal = nodo
            nodo.hijo.insert(0, raiz)
            self.dividir(nodo, 0)

    def insertar_nodo_vacio(self, raiz: Nodo, vehiculo: Vehiculo):
        contador: int = len(raiz.llave) - 1

        if (raiz.es_hoja):
            raiz.llave.append(None)

            while contador >= 0 and vehiculo.placa < raiz.llave[contador].placa:
                raiz.llave[contador + 1] = raiz.llave[contador]
                contador -= 1
            raiz.llave[contador + 1] = vehiculo
        else:
            while contador >= 0 and vehiculo.placa < raiz.llave[contador].placa:
                contador -= 1

            contador += 1

            self.insertar_nodo_vacio(raiz.hijo[contador], vehiculo) 
           
            if len(raiz.hijo[contador].llave) > self.orden - 1:  
                self.dividir(raiz, contador)



    def dividir(self, raiz: Nodo, indice: int):
        indiceMedio: int = int((self.orden - 1) / 2)    
        hijo: Nodo = raiz.hijo[indice]
        nodo: Nodo = Nodo(hijo.es_hoja)

        raiz.hijo.insert(indice + 1, nodo)

        raiz.llave.insert(indice, hijo.llave[indiceMedio])
        nodo.llave = hijo.llave[indiceMedio + 1:indiceMedio * 2 + 1]
        hijo.llave = hijo.llave[0:indiceMedio]

        if not hijo.es_hoja:
            nodo.hijo = hijo.hijo[indiceMedio + 1:indiceMedio * 2 + 2]
            hijo.hijo = hijo.hijo[0:indiceMedio+1]

    def imprimir_grafica(self):
        def añadir_nodo(graph, node, parent_id=None):
            node_id = str(id(node))

            label = " | ".join(vehiculo.placa for vehiculo in node.llave)
            graph.node(node_id, label=f"<f0> {label}", shape="record")

            if parent_id is not None:
                graph.edge(parent_id, node_id)

            for idx, child in enumerate(node.hijo):
                añadir_nodo(graph, child, parent_id=node_id)

        graph = Digraph(comment="Arbol_B", graph_attr={"rankdir": "TB"})
        añadir_nodo(graph, self.raizPricipal)

        graph.render("arbol_b_graph", format="svg", cleanup=True)

    def eliminar_vehiculo(self, placa: str):
        def eliminar_de_nodo(raiz: Nodo, placa: str):
            """Elimina la placa del nodo especificado."""
            indice = 0

            while indice < len(raiz.llave) and placa > raiz.llave[indice].placa:
                indice += 1

            if indice < len(raiz.llave) and raiz.llave[indice].placa == placa:
                if raiz.es_hoja:
                    del raiz.llave[indice]
                else:
                    eliminar_interno(raiz, indice)
            elif raiz.es_hoja:

                raise ValueError(f"La placa {placa} no se encontró en el árbol.")
            else:

                hijo = raiz.hijo[indice]

                if len(hijo.llave) == (self.orden - 1) // 2:
                    ajustar_hijo(raiz, indice)

                eliminar_de_nodo(raiz.hijo[indice], placa)

        def eliminar_interno(raiz: Nodo, indice: int):
            """Elimina la clave de un nodo interno."""
            vehiculo = raiz.llave[indice]

            if len(raiz.hijo[indice].llave) > (self.orden - 1) // 2:
                predecesor = obtener_predecesor(raiz.hijo[indice])
                raiz.llave[indice] = predecesor
                eliminar_de_nodo(raiz.hijo[indice], predecesor.placa)
            elif len(raiz.hijo[indice + 1].llave) > (self.orden - 1) // 2:
                sucesor = obtener_sucesor(raiz.hijo[indice + 1])
                raiz.llave[indice] = sucesor
                eliminar_de_nodo(raiz.hijo[indice + 1], sucesor.placa)
            else:
                fusionar(raiz, indice)
                eliminar_de_nodo(raiz.hijo[indice], vehiculo.placa)

        def obtener_predecesor(nodo: Nodo):
            actual = nodo
            while not actual.es_hoja:
                actual = actual.hijo[-1]
            return actual.llave[-1]

        def obtener_sucesor(nodo: Nodo):
            actual = nodo
            while not actual.es_hoja:
                actual = actual.hijo[0]
            return actual.llave[0]

        def ajustar_hijo(raiz: Nodo, indice: int):
            """Ajusta el hijo si tiene el número mínimo de claves."""
            if indice > 0 and len(raiz.hijo[indice - 1].llave) > (self.orden - 1) // 2:
                rotar_derecha(raiz, indice)
            elif indice < len(raiz.hijo) - 1 and len(raiz.hijo[indice + 1].llave) > (self.orden - 1) // 2:
                rotar_izquierda(raiz, indice)
            else:
                if indice < len(raiz.hijo) - 1:
                    fusionar(raiz, indice)
                else:
                    fusionar(raiz, indice - 1)

        def rotar_derecha(raiz: Nodo, indice: int):
            hijo = raiz.hijo[indice]
            hermano = raiz.hijo[indice - 1]

            hijo.llave.insert(0, raiz.llave[indice - 1])
            raiz.llave[indice - 1] = hermano.llave.pop()

            if not hijo.es_hoja:
                hijo.hijo.insert(0, hermano.hijo.pop())

        def rotar_izquierda(raiz: Nodo, indice: int):
            hijo = raiz.hijo[indice]
            hermano = raiz.hijo[indice + 1]

            hijo.llave.append(raiz.llave[indice])
            raiz.llave[indice] = hermano.llave.pop(0)

            if not hijo.es_hoja:
                hijo.hijo.append(hermano.hijo.pop(0))

        def fusionar(raiz: Nodo, indice: int):
            hijo = raiz.hijo[indice]
            hermano = raiz.hijo[indice + 1]

            hijo.llave.append(raiz.llave.pop(indice))
            hijo.llave.extend(hermano.llave)

            if not hijo.es_hoja:
                hijo.hijo.extend(hermano.hijo)

            del raiz.hijo[indice + 1]

        # delete the key from the root node
        eliminar_de_nodo(self.raizPricipal, placa)

        # if the root node is empty, make the first child the new root
        if not self.raizPricipal.llave and not self.raizPricipal.es_hoja:
            self.raizPricipal = self.raizPricipal.hijo[0]

    def buscar_vehiculo(self, placa: str):
        def buscar_en_nodo(nodo: Nodo, placa: str):
            indice = 0

            while indice < len(nodo.llave) and placa > nodo.llave[indice].placa:
                indice += 1

            if indice < len(nodo.llave) and nodo.llave[indice].placa == placa:
                return nodo.llave[indice]

            if nodo.es_hoja:
                return None

            return buscar_en_nodo(nodo.hijo[indice], placa)

        return buscar_en_nodo(self.raizPricipal, placa)

    def eliminar_vehiculo_por_placa(self, placa):
            def buscar_y_eliminar(nodo, placa):
                if nodo is None:
                    return None, False

                for i, vehiculo in enumerate(nodo.llave):
                    if vehiculo.getPlaca() == placa:

                        nodo.llave.pop(i)
                        return nodo, True

                for i, hijo in enumerate(nodo.hijo):
                    nodo.hijo[i], encontrado = buscar_y_eliminar(hijo, placa)
                    if encontrado:
                        return nodo, True

                return nodo, False

            self.raizPricipal, eliminado = buscar_y_eliminar(self.raizPricipal, placa)

            return eliminado