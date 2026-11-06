# Archivo donde vive el codigo principal del programa
from services import creacionCliente, registroCompras, consultarSaldo, consultarCatalogo, canjearUnPremio
from errors import LealtadError


# Definición del método main
def main():
    print("El programa funciona")
    opcionSeleccionada = "9"
    while opcionSeleccionada == "9":
        opcionSeleccionada = input("Seleccione el numero correspondiente a la operación deseada \n" +
                                   "1. Crear Cliente\n 2. Registrar compra\n 3. Consultar saldo\n 4. Consultar catálogo de premios\n" +
                                   "5. Canjear un premio\n 0. Salir del programa\n")
        match opcionSeleccionada:
            case "1":
                try:
                    idCliente = input("Ingrese el id del cliente: \n")
                    nombre = input("Ingrese el nombre del cliente: \n")
                    correo = input("Ingrese el correo del cliente: \n")
                    fecha = input("Ingrese la fecha de inscripción del cliente (dd-mm-aaaa): \n")
                    creacionCliente(idCliente, nombre, correo, fecha)
                    print(f"Se creo el cliente con el id: {idCliente}, nombre: {nombre}, correo: {correo} y fecha de inscripción: {fecha}\n")
                except LealtadError as e:
                    print(e.codigo)
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
                    print(f"Se registro la compra con el id: {resultado["id"]}, que genero la cantidad de: {resultado["puntos"]} " +
                          f"puntos y que dejo al usuario la cantidad de: {resultado["saldo"]}\n")
                except LealtadError as e:
                    print(e.codigo)
                    print(e)
                except Exception as e:
                    print("Ocurrio un error inesperado: " + str(e))
                opcionSeleccionada = "9"
            case "3":
                try:
                    idCliente = input("Ingrese la id del cliente cuyo saldo desea conocer: \n")
                    print(str(consultarSaldo(idCliente)) + "\n")
                except LealtadError as e:
                    print(e.codigo)
                    print(e)
                except Exception as e:
                    print("Ocurrio un error inesperado: " + str(e))
                opcionSeleccionada = "9"
            case "4":
                try:
                    catalogo = consultarCatalogo()
                    for i in catalogo:
                        print(f"id del premio: {i.idPremio}, nombre del premio: {i.nombre} " +
                              f"Costo: {i.costo}\n")
                except LealtadError as e:
                    print(e.codigo)
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
                    print(f"Se canjeo el premio con el costo de: {resultado["costo"]} puntos y que dejo al usuario la cantidad de: {resultado["saldo"]}\n")
                except LealtadError as e:
                    print(e.codigo)
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
