# Archivo donde vive el codigo principal del programa
from services import *


# Definición del método main
def main():
    print("El programa funciona")
    opcionSeleccionada = 9 
    while not opcionSeleccionada == 9:
        opcionSeleccionada = input ("Seleccione el numero correspondiente a la operación deseada \n"+
                                "1. Crear Cliente\n 2. Registrar compra\n 3. Consultar saldo\n 4. Consultar catálogo de premios\n" +
                                "5. Canjear un premio\n 0. Salir del programa\n")
        match opcionSeleccionada:
            case 1:
                try:
                    idCliente = input("Ingrese el id del cliente: ")
                    nombre = input("Ingrese el nombre del cliente: ")
                    correo = input("Ingrese el correo del cliente: ")
                    fecha = input("Ingrese la fecha de inscripción del cliente (dd-mm-aaaa): ")
                    creacionCliente(idCliente, nombre, correo, fecha)
                except Exception as e:
                    print(e)
                opcionSeleccionada = 9
            case 2:
                try:
                    idCliente = input("Ingrese el id del cliente: ")
                    monto = input("Ingrese el monto de la compra: ")
                    fecha = input("Ingrese la fecha de inscripción de la compra (dd-mm-aaaa): ")
                    resultado=registroCompras(idCliente, monto, fecha)
                    print (f"Se registro la compra con el id: {resultado[id]}, que genero la cantidad de: {resultado[puntos]}" +
                           f"puntos y que dejo al usuario la cantidad de{resultado[saldo]}")
                except Exception as e:
                    print (e)
                opcionSeleccionada = 9
            case 3:
                try:
                    idCliente = input("")
                except Exception as e:
                    print(e)
            case 4: # Puedes agrupar casos con la barra vertical
                print("Elegiste la opción 3 o 4")
            case _:
                print("Opción por defecto (no válida)")
