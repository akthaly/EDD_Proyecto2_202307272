class Viaje:
    def __init__(self, cliente, vehiculo, ruta, fecha_hora_inicio, viaje_id):
        self.cliente = cliente  # Apuntador al cliente (de la lista circular)
        self.vehiculo = vehiculo  # Apuntador al vehículo (del árbol B)
        self.ruta = ruta  # Lista simple que representa la ruta tomada
        self.fecha_hora_inicio = fecha_hora_inicio  # Fecha y hora de inicio proporcionada como parámetro
        self.viaje_id = viaje_id  # ID único del viaje

    def __str__(self):
        ruta_str = str(self.ruta) 
        return (f"Viaje - Cliente: {self.cliente.getNombre()} {self.cliente.getApellido()}\n"
                f"Vehículo: {self.vehiculo.getPlaca()}\n"
                f"Fecha y Hora de Inicio: {self.fecha_hora_inicio}\n"
                f"Ruta: {ruta_str}")

    def get_id(self):
        return self.viaje_id

    def getCliente(self):
        return self.cliente

    def getVehiculo(self):
        return self.vehiculo

    def getRuta(self):
        return self.ruta

    def getFechaHoraInicio(self):
        return self.fecha_hora_inicio

    def setCliente(self, cliente):
        self.cliente = cliente

    def setVehiculo(self, vehiculo):
        self.vehiculo = vehiculo

    def setRuta(self, ruta):
        self.ruta = ruta

    def setFechaHoraInicio(self, fecha_hora_inicio):
        self.fecha_hora_inicio = fecha_hora_inicio
