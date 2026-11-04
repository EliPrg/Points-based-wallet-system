# Archivo para la definición de errores personalizados

# Clase para las excepciones de un cliente duplicado
class ErrorClienteDup(Exception):
    # Constructor de la clase
    def __init__(self, idCliente):
        super().__init__(idCliente)
        self.idCliente = idCliente

    # Metodo para la impresión del mensaje de la excepción
    def __str__(self):
        return (f"Ya existe un cliente con la id: {self.idCliente}")


# Clase para las excepciones de cliente no encontrados
class ErrorClienteNoEncontrado(Exception):
    # Constructor de la clase
    def __init__(self, idCliente):
        super().__init__(idCliente)
        self.idCliente = idCliente
    
    # Metodo para la impresión del mensaje de la excepción
    def __str__(self):
        return (f"El cliente con la id: {self.idCliente} no fue encontrado")


# Clase para las excepciones de cliente no encontrados
class ErrorDatosInvalidos(Exception):
    # Constructor de la clase
    def __init__(self, zona_error, dato_invalido):
        super().__init__(zona_error, dato_invalido)
        self.zona_error = zona_error
        self.dato_invalido = dato_invalido

    # Metodo para la impresión del mensaje de la excepción
    def __str__(self):
        return (f"Datos invalido: {self.DatoInvalido} No cumple con el formato solicitado en el {self.ZonaError}")
