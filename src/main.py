# Archivo donde vive el codigo principal del programa
from services import creacionCliente, registroCompras, consultarSaldo, consultarCatalogo, canjearUnPremio, consultarNivel, consultarHistorial
from errors import LealtadError


# Definición del método main
def main():
    print("El programa funciona")
    opcionSeleccionada = "9"
    while opcionSeleccionada == "9":
        opcionSeleccionada = input("Seleccione el numero correspondiente a la operación deseada \n" +
                                   "1. Crear Cliente\n2. Registrar compra\n3. Consultar saldo\n4. Consultar catálogo de premios\n" +
                                   "5. Canjear un premio\n6. Consultar nivel\n7. Consultar historial\n0. Salir del programa\n")
        match opcionSeleccionada:
            case "1":
                try:
                    idCliente = input("Ingrese el id del cliente: \n")
                    nombre = input("Ingrese el nombre del cliente: \n")
                    correo = input("Ingrese el correo del cliente: \n")
                    fecha = input("Ingrese la fecha de inscripción del cliente (dd-mm-aaaa): \n")
                    creacionCliente(idCliente, nombre, correo, fecha)
                    print(f"Se creo el cliente con el id: {idCliente}, nombre: {nombre}, correo: {correo} y fecha de inscripción: {fecha}\n\n")
                except LealtadError as e:
                    print(e.codigo + "\n")
                    print(e)
                except Exception as e:
                    print("Ocurrio un error inesperado: " + str(e))
                opcionSeleccionada = "9"
            case "2":
                try:
                    idCliente = input("Ingrese el id del cliente: \n")
                    monto = input("Ingrese el monto de la compra: \n")
                    fecha = input("Ingrese la fecha de inscripción de la compra (dd-mm-aaaa): \n")
                    resultado = registroCompras(idCliente, monto, fecha)
                    print(f"Se registro la compra con el id: {resultado['id']}, que genero la cantidad de: {resultado['puntos']} " +
                          f"puntos y que dejo al usuario la cantidad de: {resultado['saldo']}, el nivel utilizado fue: {resultado['nivel']} " +
                          f" y el multiplicador fue{resultado['mul']}\n\n")
                except LealtadError as e:
                    print(e.codigo + "\n")
                    print(e)
                except Exception as e:
                    print("Ocurrio un error inesperado: " + str(e))
                opcionSeleccionada = "9"
            case "3":
                try:
                    idCliente = input("Ingrese la id del cliente cuyo saldo desea conocer: \n")
                    print(str(consultarSaldo(idCliente)) + "\n\n")
                except LealtadError as e:
                    print(e.codigo + "\n")
                    print(e)
                except Exception as e:
                    print("Ocurrio un error inesperado: " + str(e))
                opcionSeleccionada = "9"
            case "4":
                try:
                    catalogo = consultarCatalogo()
                    for i in catalogo:
                        print(f"id del premio: {i.idPremio}, nombre del premio: {i.nombre} " +
                              f"Costo: {i.costo}\n\n")
                except LealtadError as e:
                    print(e.codigo + "\n")
                    print(e)
                except Exception as e:
                    print("Ocurrio un error inesperado: " + str(e))
                opcionSeleccionada = "9"
            case "5":
                try:
                    idCliente = input("Ingrese el id del cliente: \n")
                    idPremio = input("Ingrese el id del premio que desea canjear: \n")
                    fecha = input("Ingrese la fecha de inscripción del canje (dd-mm-aaaa): \n")
                    resultado = canjearUnPremio(idCliente, idPremio, fecha)
                    print(f"Se canjeo el premio con el costo de: {resultado['costo']} puntos y que dejo al usuario la cantidad de: {resultado['saldo']}\n\n")
                except LealtadError as e:
                    print(e.codigo + "\n")
                    print(e)
                except Exception as e:
                    print("Ocurrio un error inesperado: " + str(e))
                opcionSeleccionada = "9"
            case "6":
                try:
                    idCliente = input("Ingrese el id del cliente: \n")
                    nivel = consultarNivel(idCliente)
                    print(f"El nivel del cliente es: {nivel['nivel']}, los puntos acumulados son: {nivel['puntosAcum']} y faltan: {nivel['difNivel']} " +
                          "para el siguiente nivel\n\n")
                except LealtadError as e:
                    print(e.codigo + "\n")
                    print(e)
                except Exception as e:
                    print("Ocurrio un error inesperado: " + str(e))
                opcionSeleccionada = "9"
            case "7":
                try:
                    idCliente = input("Ingrese el id del cliente: \n")
                    historial = consultarHistorial(idCliente)
                    print("TIPO DE MOVIMIENTO | PUNTOS | FECHA | REFERENCIA\n")
                    for movimiento in historial:
                        print(f"Tipo: {movimiento['tipo']}, Puntos: {movimiento['puntos']}, Fecha: {movimiento['fecha']}, Referencia: {movimiento['referencia']}\n\n")
                except LealtadError as e:
                    print(e.codigo + "\n")
                    print(e)
                except Exception as e:
                    print("Ocurrio un error inesperado: " + str(e))
                opcionSeleccionada = "9"
            case "0":
                print("Saliendo del programa")
            case _:
                print("El caracter añadido no es valido, por favor ingrese un numero valido\n")
                opcionSeleccionada = "9"


if __name__ == "__main__":
    main()
