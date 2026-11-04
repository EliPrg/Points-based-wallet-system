# Archivo para la definición de errores personalizados

# Clase para las excepciones de un cliente duplicado
class ErrorClienteDuplicado(Exception):
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


# Clase para las excepciones de datos inválidos
class ErrorDatosInvalidos(Exception):
    # Constructor de la clase
    def __init__(self, zonaError, datoInvalido):
        super().__init__(zonaError, datoInvalido)
        self.zonaError = zonaError
        self.datoInvalido = datoInvalido

    # Metodo para la impresión del mensaje de la excepción
    def __str__(self):
        return (f"Datos invalido: {self.datoInvalido} No cumple con el formato solicitado en el {self.zonaError}")


# Clase para las excepciones de fecha Invalida
class ErrorFechaInvalida(Exception):
    # Constructor de la clase
    def __init__(self, fecha, motivoDeInvalidez):
        super().__init__(fecha, motivoDeInvalidez)
        self.fecha = fecha
        self.motivoDeInvalidez = motivoDeInvalidez

    # Metodo para la impresión del mensaje de la excepción
    def __str__(self):
        return (f"La fecha: {self.fecha} es invalida debido a que {self.motivoDeInvalidez}")


# Clase para las excepciones de premio no encontrados
class ErrorPremioNoEncontrado(Exception):
    # Constructor de la clase
    def __init__(self, idPremio):
        super().__init__(idPremio)
        self.idPremio = idPremio

    # Metodo para la impresión del mensaje de la excepción
    def __str__(self):
        return (f"El premio con la id: {self.idPremio} no fue encontrado")


# Clase para las excepciones de premio sin stock
class ErrorPremioSinStock(Exception):
    # Constructor de la clase
    def __init__(self, nombre):
        super().__init__(nombre)
        self.nombre = nombre

    # Metodo para la impresión del mensaje de la excepción
    def __str__(self):
        return (f"El premio '{self.nombre}' no tiene stock disponible")