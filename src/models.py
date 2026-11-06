# Definición de costantes para el sistema
from dataclasses import dataclass
import datetime
from decimal import Decimal


# Clase cliente
@dataclass()
class cliente:
    idCliente: str
    nombre: str
    correo: str
    fechaIns: datetime
    nivel: str = ("Bronce", Decimal("1.00"))
    saldo: int = 0
    puntosAcum: int = 0


# Clase para compras
@dataclass()
class compras:
    idCompra: str
    idCliente: str
    monto: float
    fecha: datetime
    puntos: int


# Canje premio
@dataclass()
class canjePremio:
    idCanje: str
    idCliente: str
    idPremio: str
    fecha: datetime
    puntos: int
