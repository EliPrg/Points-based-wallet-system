# Archivo de servicios para el sistema de lealtad
from config import Catalogo
from models import cliente, compras, canjePremio
from validations import validarDatosCliente, validarDatosCompra, validarExistenciaCliente, validarDatosCanjePremio
from calculations import calcularPuntosAcum, calcularNivel, difProximoNivel
from datetime import datetime
from decimal import Decimal
from calculations import buscarPremio
clientes = {}
fechas = []
listaCompras = {}
listaCanjes = {}
stockPremios = {
     p.idPremio: p.stockInicial for p in Catalogo
}


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
    nivelUsado = clientes[idCliente].nivel
    puntosSum = calcularPuntosAcum(monto, nivelUsado[1])
    idCompra = "C-" + str(len(listaCompras) + 1)
    # Creación de la nueva compra y almacenamiento en el diccionario de compras
    nuevaCompra = compras(idCompra, idCliente, Decimal(monto), fecha)
    clientes[idCliente].saldo += puntosSum
    clientes[idCliente].puntosAcum += puntosSum
    clientes[idCliente].nivel = calcularNivel(clientes[idCliente].puntosAcum)
    listaCompras[nuevaCompra.idCompra] = nuevaCompra
    fechas.append(fecha)
    # Retorno de la nueva compra creada
    return ({"id": idCompra, "puntos": puntosSum, "saldo": clientes[idCliente].saldo, "nivel": nivelUsado[0], "mul": nivelUsado[1]})


def consultarSaldo(idCliente: str):
    validarExistenciaCliente(idCliente, clientes)
    return (clientes[idCliente].saldo)


def consultarCatalogo():
    return (list(Catalogo))


def canjearUnPremio(idCliente: str, idPremio: str, fecha: str):
    validarExistenciaCliente(idCliente, clientes)
    # Validación de existencia del premio en el catalogo
    validarDatosCanjePremio(idCliente, clientes, idPremio, fecha, fechas, stockPremios)
    premio = buscarPremio(idPremio)
    clientes[idCliente].saldo -= premio.costo
    stockPremios[idPremio] -= 1
    fecha = datetime.strptime(fecha, "%d-%m-%Y").date()
    nuevoCanje = canjePremio(idCliente, idPremio, fecha)
    listaCanjes[nuevoCanje.fecha] = nuevoCanje
    fechas.append(fecha)
    return {"costo": premio.costo, "saldo": clientes[idCliente].saldo}


# Método para consultar el nivel de un cliente
def consultarNivel(idCliente):
    validarExistenciaCliente(idCliente, clientes)
    return {"nivel": clientes[idCliente].nivel[0], "puntosAcum": clientes[idCliente].nivel[1], "difNivel": difProximoNivel(clientes[idCliente].puntosAcum)}
