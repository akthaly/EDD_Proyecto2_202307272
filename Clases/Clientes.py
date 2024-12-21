class Clientes():
    def __init__ (self, dpi, nombres, apellidos, genero, telefono, direccion):
        self.dpi = dpi
        self.nombre = nombres
        self.apellido = apellidos
        self.genero = genero
        self.telefono = telefono
        self.direccion = direccion

    def getDPI(self):
        return self.dpi
    
    def getNombre(self):
        return self.nombre
    
    def getApellido(self):
        return self.apellido
    
    def getGenero(self):
        return self.genero
    
    def getTelefono(self):
        return self.telefono
    
    def getDireccion(self):
        return self.direccion
    
    def setDPI(self, dpi):
        self.dpi = dpi

    def setNombre(self, nombres):
        self.nombre = nombres

    def setApellido(self, apellidos):
        self.apellido = apellidos

    def setGenero(self, genero):
        self.genero = genero

    def setTelefono(self, telefono):
        self.telefono = telefono

    def setDireccion(self, direccion):
        self.direccion = direccion

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