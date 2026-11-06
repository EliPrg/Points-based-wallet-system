# Pruebas automatizadas del nivel 1 (secciones 10.1, 10.2, 10.4 y 10.5 del enunciado)
import importlib
import unittest

import services
from errors import LealtadError


class PruebaBase(unittest.TestCase):
    # Cada prueba parte de un estado limpio, igual que reiniciar el programa
    def setUp(self):
        importlib.reload(services)

    # Comprueba que la operación lance un error con el código esperado
    def assertCodigo(self, codigo, funcion, *args):
        with self.assertRaises(LealtadError) as contexto:
            funcion(*args)
        self.assertEqual(contexto.exception.codigo, codigo)


class TestPrueba1AltaDeClientes(PruebaBase):
    def test_flujo_completo(self):
        # 1. Crear cliente
        cliente = services.creacionCliente("C001", "Ana Pérez", "ana@correo.com", "05-01-2026")
        self.assertEqual(cliente.idCliente, "C001")
        # 2. Cliente duplicado
        self.assertCodigo("CLIENTE_DUPLICADO", services.creacionCliente,
                          "C001", "Ana Pérez", "ana@correo.com", "05-01-2026")
        # 3. Nombre vacío
        self.assertCodigo("DATOS_INVALIDOS", services.creacionCliente,
                          "C002", "", "luis@correo.com", "05-01-2026")
        # 4. Correo sin @
        self.assertCodigo("DATOS_INVALIDOS", services.creacionCliente,
                          "C002", "Luis Gómez", "luis.correo.com", "05-01-2026")
        # 5. Saldo inicial
        self.assertEqual(services.consultarSaldo("C001"), 0)
        # 6. Cliente inexistente
        self.assertCodigo("CLIENTE_NO_ENCONTRADO", services.consultarSaldo, "C999")
        # 7. Catálogo
        catalogo = services.consultarCatalogo()
        self.assertEqual(len(catalogo), 5)
        self.assertEqual([p.costo for p in catalogo], [100, 250, 800, 1200, 4000])

    def test_nombre_solo_espacios(self):
        self.assertCodigo("DATOS_INVALIDOS", services.creacionCliente,
                          "C001", "   ", "ana@correo.com", "05-01-2026")

    def test_id_vacio_o_nulo(self):
        self.assertCodigo("DATOS_INVALIDOS", services.creacionCliente,
                          "", "Ana Pérez", "ana@correo.com", "05-01-2026")
        self.assertCodigo("DATOS_INVALIDOS", services.creacionCliente,
                          None, "Ana Pérez", "ana@correo.com", "05-01-2026")

    def test_creacion_fallida_no_deja_cliente(self):
        self.assertCodigo("DATOS_INVALIDOS", services.creacionCliente,
                          "C002", "", "luis@correo.com", "05-01-2026")
        self.assertCodigo("CLIENTE_NO_ENCONTRADO", services.consultarSaldo, "C002")


class TestPrueba2ComprasYCanjes(PruebaBase):
    def setUp(self):
        super().setUp()
        services.creacionCliente("C001", "Ana Pérez", "ana@correo.com", "05-01-2026")

    def test_flujo_completo(self):
        # 2. Compra de 500.00
        r = services.registroCompras("C001", "500.00", "10-01-2026")
        self.assertEqual((r["id"], r["puntos"], r["saldo"]), ("C-1", 50, 50))
        # 3. Compra de 1234.50 (redondeo hacia abajo)
        r = services.registroCompras("C001", "1234.50", "11-01-2026")
        self.assertEqual((r["id"], r["puntos"], r["saldo"]), ("C-2", 123, 173))
        # 4. Compra de 9.99: se registra con 0 puntos
        r = services.registroCompras("C001", "9.99", "12-01-2026")
        self.assertEqual((r["id"], r["puntos"], r["saldo"]), ("C-3", 0, 173))
        # 5 y 6. Montos inválidos
        self.assertCodigo("MONTO_INVALIDO", services.registroCompras, "C001", "-5.00", "12-01-2026")
        self.assertCodigo("MONTO_INVALIDO", services.registroCompras, "C001", "10.555", "12-01-2026")
        # 7. Canje exitoso de P01
        r = services.canjearUnPremio("C001", "P01", "15-01-2026")
        self.assertEqual((r["costo"], r["saldo"]), (100, 73))
        # 8. Saldo insuficiente: el saldo no cambia
        self.assertCodigo("SALDO_INSUFICIENTE", services.canjearUnPremio, "C001", "P02", "15-01-2026")
        self.assertEqual(services.consultarSaldo("C001"), 73)
        # 9. Premio inexistente
        self.assertCodigo("PREMIO_NO_ENCONTRADO", services.canjearUnPremio, "C001", "P99", "15-01-2026")
        # 10. Saldo final
        self.assertEqual(services.consultarSaldo("C001"), 73)

    def test_cliente_inexistente_en_compra_y_canje(self):
        self.assertCodigo("CLIENTE_NO_ENCONTRADO", services.registroCompras, "C999", "100.00", "10-01-2026")
        self.assertCodigo("CLIENTE_NO_ENCONTRADO", services.canjearUnPremio, "C999", "P01", "10-01-2026")

    def test_montos_validos_sin_decimales_o_con_un_decimal(self):
        self.assertEqual(services.registroCompras("C001", "500", "10-01-2026")["puntos"], 50)
        self.assertEqual(services.registroCompras("C001", "100.5", "11-01-2026")["puntos"], 10)

    def test_montos_invalidos_no_numericos(self):
        for monto in ("abc", "", "0", "NaN", "Infinity", None):
            with self.subTest(monto=monto):
                self.assertCodigo("MONTO_INVALIDO", services.registroCompras, "C001", monto, "10-01-2026")
        self.assertEqual(services.consultarSaldo("C001"), 0)

    def test_ids_de_compra_consecutivos_y_sin_huecos_tras_un_error(self):
        self.assertEqual(services.registroCompras("C001", "100.00", "10-01-2026")["id"], "C-1")
        self.assertCodigo("MONTO_INVALIDO", services.registroCompras, "C001", "-1", "10-01-2026")
        self.assertEqual(services.registroCompras("C001", "100.00", "10-01-2026")["id"], "C-2")


class TestPrueba4CanjesSucesivos(PruebaBase):
    def test_canjes_sucesivos_y_atomicidad(self):
        # 1 y 2. Cliente con 8000 puntos
        services.creacionCliente("C001", "Jorge Mora", "jorge@correo.com", "01-03-2026")
        r = services.registroCompras("C001", "80000.00", "02-03-2026")
        self.assertEqual((r["id"], r["puntos"], r["saldo"]), ("C-1", 8000, 8000))
        # 3 y 4. Dos canjes de P05
        self.assertEqual(services.canjearUnPremio("C001", "P05", "03-03-2026")["saldo"], 4000)
        self.assertEqual(services.canjearUnPremio("C001", "P05", "04-03-2026")["saldo"], 0)
        # 5. El tercero falla
        self.assertCodigo("SALDO_INSUFICIENTE", services.canjearUnPremio, "C001", "P05", "05-03-2026")
        # 6. El canje fallido no cambió nada
        self.assertEqual(services.consultarSaldo("C001"), 0)

    def test_canjes_el_mismo_dia(self):
        services.creacionCliente("C001", "Jorge Mora", "jorge@correo.com", "01-03-2026")
        services.registroCompras("C001", "10000.00", "02-03-2026")
        self.assertEqual(services.canjearUnPremio("C001", "P01", "03-03-2026")["saldo"], 900)
        self.assertEqual(services.canjearUnPremio("C001", "P01", "03-03-2026")["saldo"], 800)
        self.assertEqual(services.consultarSaldo("C001"), 800)


class TestPrueba5FechasEInvalidos(PruebaBase):
    def setUp(self):
        super().setUp()
        services.creacionCliente("C001", "Sofía Rojas", "sofia@correo.com", "01-03-2026")

    def test_flujo_completo(self):
        # 2. Compra válida
        r = services.registroCompras("C001", "200.00", "10-03-2026")
        self.assertEqual((r["id"], r["puntos"], r["saldo"]), ("C-1", 20, 20))
        # 3. Fecha anterior a la última operación
        self.assertCodigo("FECHA_INVALIDA", services.registroCompras, "C001", "100.00", "05-03-2026")
        # 4. Fecha inexistente
        self.assertCodigo("FECHA_INVALIDA", services.registroCompras, "C001", "100.00", "30-02-2026")
        # 5. Monto escrito como texto
        self.assertCodigo("MONTO_INVALIDO", services.registroCompras, "C001", "abc", "11-03-2026")
        # 7. Ninguna operación fallida modificó el saldo
        self.assertEqual(services.consultarSaldo("C001"), 20)

    def test_formatos_de_fecha_invalidos(self):
        for fecha in ("5-1-2026", "2026-03-10", "10/03/2026", "abc", "", None):
            with self.subTest(fecha=fecha):
                self.assertCodigo("FECHA_INVALIDA", services.registroCompras, "C001", "100.00", fecha)

    def test_fecha_igual_a_la_ultima_es_valida(self):
        services.registroCompras("C001", "100.00", "10-03-2026")
        self.assertEqual(services.registroCompras("C001", "100.00", "10-03-2026")["id"], "C-2")

    def test_operacion_fallida_no_adelanta_la_fecha(self):
        # Una compra rechazada por monto no debe registrar su fecha como "última operación"
        self.assertCodigo("MONTO_INVALIDO", services.registroCompras, "C001", "-5.00", "20-03-2026")
        self.assertEqual(services.registroCompras("C001", "100.00", "11-03-2026")["puntos"], 10)

    def test_la_fecha_aplica_a_todas_las_operaciones(self):
        services.registroCompras("C001", "1000.00", "10-03-2026")
        self.assertCodigo("FECHA_INVALIDA", services.canjearUnPremio, "C001", "P01", "09-03-2026")
        self.assertCodigo("FECHA_INVALIDA", services.creacionCliente,
                          "C002", "Luis Gómez", "luis@correo.com", "09-03-2026")


class TestAislamientoEntreClientes(PruebaBase):
    def test_operaciones_de_un_cliente_no_afectan_a_otro(self):
        services.creacionCliente("C001", "Ana Pérez", "ana@correo.com", "05-01-2026")
        services.creacionCliente("C002", "Luis Gómez", "luis@correo.com", "05-01-2026")
        services.registroCompras("C001", "1000.00", "06-01-2026")
        services.canjearUnPremio("C001", "P01", "07-01-2026")
        self.assertEqual(services.consultarSaldo("C001"), 0)
        self.assertEqual(services.consultarSaldo("C002"), 0)


if __name__ == "__main__":
    unittest.main()