class Rutas():
    def __init__(self, origen, destino, tiempo_de_ruta):
        self.origen = origen
        self.destino = destino
        self.tiempo_de_ruta = tiempo_de_ruta

    def getOrigen(self):
        return self.origen
    
    def getDestino(self):
        return self.destino
    
    def getTiempoDeRuta(self):
        return self.tiempo_de_ruta
    
    def setOrigen(self, origen):
        self.origen = origen

    def setDestino(self, destino):
        self.destino = destino

    def setTiempoDeRuta(self, tiempo_de_ruta):
        self.tiempo_de_ruta = tiempo_de_ruta

    def agregar(self):
        pass

    def modificar(self, llave):
        pass

    def eliminar(self, llave):
        pass

    def mostrar_info(self, llave):
        pass

    def mostrar_estructura_datos(self):
        pass