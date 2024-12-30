class Vehiculo():
    def __init__ (self, placa, marca, modelo, precio_por_segundo):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.precio_por_segundo = precio_por_segundo

    def __str__(self):
        return f"Placa: {self.placa}, Marca: {self.marca}, Modelo: {self.modelo}, Precio por segundo: {self.precio_por_segundo}"


    def getPlaca(self):
        return self.placa
    
    def getMarca(self):
        return self.marca
    
    def getModelo(self):
        return self.modelo
    
    def getPrecioPorSegundo(self):
        return self.precio_por_segundo
    
    def setPlaca(self, placa):
        self.placa = placa

    def setMarca(self, marca):
        self.marca = marca

    def setModelo(self, modelo):
        self.modelo = modelo

    def setPrecioPorSegundo(self, precio_por_segundo):
        self.precio_por_segundo = precio_por_segundo

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

