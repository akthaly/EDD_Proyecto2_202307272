class Viajes():
    def __init__(self, origen, destino, fecha_hora_inicio):
        self.origen = origen
        self.destino = destino
        self.fecha_hora_inicio = fecha_hora_inicio
    

    def getOrigen(self):
        return self.origen
    
    def getDestino(self):
        return self.destino
    
    def getFechaHoraInicio(self):
        return self.fecha_hora_inicio
    
    def setOrigen(self, origen):
        self.origen = origen

    def setDestino(self, destino):
        self.destino = destino

    def setFechaHoraInicio(self, fecha_hora_inicio):
        self.fecha_hora_inicio = fecha_hora_inicio

    def agregar(self):
        pass

    def mostrar_estructura_datos(self):
        pass