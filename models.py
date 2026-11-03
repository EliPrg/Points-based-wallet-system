# Definición de costantes para el sistema
from dataclasses import dataclass
import datetime


# Clase cliente 
@dataclass()
class cliente:
    idCliente: str
    nombre: str
    correo: str
    saldo: int
    puntosAcum: int


#Clase para compras
@dataclass()
class compras:
    idCompra: str
    idCliente: str
    monto: float
    fecha: datetime


#Canje premio
@dataclass()
class canjePremio:
    idCanje: str
    idCliente: str
    idPremio: str
    fecha: datetime
