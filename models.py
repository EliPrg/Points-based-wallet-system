# Definición de costantes para el sistema
from dataclasses import dataclass
import datetime


# Clase cliente
@dataclass()
class cliente:
    idCliente: str
    nombre: str
    correo: str
    saldo: int = 0
    puntosAcum: int = 0
    fechaIns: datetime


# Clase para compras
@dataclass()
class compras:
    idCompra: str
    idCliente: str
    monto: float
    fecha: datetime


# Canje premio
@dataclass()
class canjePremio:
    idCanje: str
    idCliente: str
    idPremio: str
    fecha: datetime
