# Archivo de servicios para el sistema de lealtad
from config import Catalogo
from models import cliente, compras
from validations import validarDatosCliente, validarDatosCompra, validarExistenciaCliente
from calculations import calcularPuntosAcum
from datetime import datetime
from decimal import Decimal
clientes = {}
fechas = []
listaCompras = {}


def creacionCliente(idCliente: str, nombre: str, correoElectronico: str, fecha: str):
    validarDatosCliente(idCliente, nombre, correoElectronico, clientes, fecha, fechas)
    fecha = datetime.strptime(fecha, "%d-%m-%Y").date()
    nuevoCliente = cliente(idCliente, nombre, correoElectronico, fecha)
    fechas.append(fecha)
    clientes[nuevoCliente.idCliente] = nuevoCliente
    return (nuevoCliente)


def registroCompras(idCliente: str, monto: str, fecha: str):
    # Validación los datos de entrada de la compra
    validarDatosCompra(idCliente, clientes, fecha, fechas, monto)
    fecha = datetime.strptime(fecha, "%d-%m-%Y").date()
    puntosSum = calcularPuntosAcum(monto)
    idCompra = "C-" + str(len(listaCompras) + 1)
    # Creación de la nueva compra y almacenamiento en el diccionario de compras
    nuevaCompra = compras(idCompra, idCliente, Decimal(monto), fecha)
    clientes[idCliente].saldo += puntosSum
    clientes[idCliente].puntosAcum += puntosSum
    listaCompras[nuevaCompra.idCompra] = nuevaCompra
    fechas.append(fecha)
    # Retorno de la nueva compra creada
    return ({"id de la Compra": idCompra, "puntos sumados": puntosSum, "Saldo final del cliente": clientes[idCliente].saldo})


def consultarSaldo(idCliente: str):
    validarExistenciaCliente(idCliente, clientes)
    return (clientes[idCliente].saldo)


def consultarCatalogo():
    for i in len(Catalogo):
        for j in len(Catalogo[i]):
            print(f"id: {Catalogo[i, j].id_premio}, Nombre: {Catalogo[i, j].nombre}, Costo: {Catalogo[i, j].costo}")


def canjePremio(idCanje: str, idCliente: str, idPremio: str, fecha: datetime):
    canjePremio(idCanje, idCliente, idPremio, fecha)
