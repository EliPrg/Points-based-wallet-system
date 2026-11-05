# Archivo de servicios para el sistema de lealtad
from config import Catalogo
from models import cliente, compras
from validations import validarDatosCliente
from datetime import datetime
clientes = {}
fechas =  []


def creacionCliente(idCliente: str, nombre: str, correoElectronico: str, fecha: str):
    validarDatosCliente(idCliente, nombre, correoElectronico, clientes, fecha, fechas)
    fecha = datetime.strptime(fecha, "%d-%m-%Y").date()
    nuevoCliente = cliente(idCliente, nombre, correoElectronico, fecha)
    fechas.append(fecha)
    clientes[nuevoCliente.idCliente] = nuevoCliente
    return (nuevoCliente)


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
