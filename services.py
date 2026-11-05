# Archivo de servicios para el sistema de lealtad
from config import Catalogo
from models import cliente, compras
import datetime


def creaciónCliente(idCliente: str, nombre: str, correoElectronico: str):
    cliente(idCliente, nombre, correoElectronico)


def registroCompras(idCompra: str, idCliente: str, monto: float, fecha: datetime):
    compras(idCompra, idCliente, monto, fecha)


def consultarSaldo(idCliente: str):
    return ()


def consultarCatalogo():
    for i in len(Catalogo):
        for j in len(Catalogo[i]):
            print(f"id: {Catalogo[i, j].id_premio}, Nombre: {Catalogo[i, j].nombre}, Costo: {Catalogo[i, j].costo}")


def canjePremio(idCanje: str, idCliente: str, idPremio: str, fecha: datetime):
    canjePremio(idCanje, idCliente, idPremio, fecha)
