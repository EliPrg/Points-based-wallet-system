# Archivo de servicios para el sistema de lealtad
from config import Niveles, UM_puntos, Catalogo
from models import cliente, compras
import datetime

# Arreglo de clientes
cliente = {}

# Arreglo de compras
compras = {}


def calcularPuntosAcum(monto: float):
    return((monto/UM_puntos)*1)


def creaciónCliente(idCliente: str, nombre: str, correoElectronico: str):
    cliente(idCliente, nombre, correoElectronico)


def registroCompras(idCompra: str, idCliente: str, monto: float, fecha: datetime):
    compras(idCompra, idCliente, monto, fecha)


def consultarSaldo(idCliente: str):
    return()


def consultarCatalogo():
    for i in len(Catalogo):
        for l in len(Catalogo[i]):
            print(f"id: {Catalogo[i,l].id_premio}, Nombre: {Catalogo[i,l].nombre}, Costo: {Catalogo[i,l].costo} ")


def canjePremio(idCanje: str, idCliente: str, idPremio: str, fecha: datetime):
    canjePremio(idCanje, idCliente, idPremio, fecha)
