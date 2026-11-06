# Pruebas automatizadas del nivel 2 (secciones 10.3, 10.4 y 10.5 del enunciado: niveles, multiplicador e historial)
import importlib
import unittest
from datetime import date
from decimal import Decimal

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

    # Comprueba el resultado de registrar una compra: id, puntos, saldo, nivel y multiplicador aplicados
    def assertCompra(self, resultado, idCompra, puntos, saldo, nivel, multiplicador):
        self.assertEqual(resultado["id"], idCompra)
        self.assertEqual(resultado["puntos"], puntos)
        self.assertEqual(resultado["saldo"], saldo)
        self.assertEqual(resultado["nivel"], nivel)
        self.assertEqual(Decimal(str(resultado["mul"])), Decimal(multiplicador))

    # Comprueba el resultado de consultar el nivel
    def assertNivel(self, idCliente, nivel, puntosAcum, faltan):
        r = services.consultarNivel(idCliente)
        self.assertEqual(r["nivel"], nivel)
        self.assertEqual(r["puntosAcum"], puntosAcum)
        self.assertEqual(str(r["difNivel"]), faltan)

    # Comprueba que la suma de los movimientos del historial coincida con el saldo
    def assertHistorialCoincideConSaldo(self, idCliente):
        suma = sum(m["puntos"] for m in services.consultarHistorial(idCliente))
        self.assertEqual(suma, services.consultarSaldo(idCliente))


class TestPrueba3NivelesYMultiplicador(PruebaBase):
    def test_flujo_completo(self):
        # 1. Crear cliente
        services.creacionCliente("C001", "Marta Ruiz", "marta@correo.com", "01-02-2026")
        # 2. Compra de 9000.00: Bronce, 900 puntos
        self.assertCompra(services.registroCompras("C001", "9000.00", "01-02-2026"), "C-1", 900, 900, "Bronce", "1.00")
        # 3. Consultar nivel: le faltan 100 para Plata
        self.assertNivel("C001", "Bronce", 900, "100")
        # 4. Compra de 1000.00: cruza el umbral pero aplica el multiplicador del nivel anterior
        self.assertCompra(services.registroCompras("C001", "1000.00", "02-02-2026"), "C-2", 100, 1000, "Bronce", "1.00")
        # 5. Consultar nivel: ya es Plata, le faltan 4000 para Oro
        self.assertNivel("C001", "Plata", 1000, "4000")
        # 6. Compra de 400.00: Plata x1.25
        self.assertCompra(services.registroCompras("C001", "400.00", "03-02-2026"), "C-3", 50, 1050, "Plata", "1.25")
        # 7. Compra de 38.00: 3.8 x 1.25 = 4.75, se redondea a 4
        self.assertCompra(services.registroCompras("C001", "38.00", "04-02-2026"), "C-4", 4, 1054, "Plata", "1.25")
        # 8. Compra de 40000.00: Plata x1.25, 5000 puntos
        self.assertCompra(services.registroCompras("C001", "40000.00", "05-02-2026"), "C-5", 5000, 6054, "Plata", "1.25")
        # 9. Consultar nivel: ya es Oro, no le falta nada
        r = services.consultarNivel("C001")
        self.assertEqual((r["nivel"], r["puntosAcum"]), ("Oro", 6054))
        self.assertFalse(str(r["difNivel"]).isdigit())
        # 10. Compra de 133.30: 13.33 x 1.5 = 19.995, se redondea a 19
        self.assertCompra(services.registroCompras("C001", "133.30", "06-02-2026"), "C-6", 19, 6073, "Oro", "1.50")
        # 11. Canjear P05 (4000 puntos)
        self.assertEqual(services.canjearUnPremio("C001", "P05", "07-02-2026")["saldo"], 2073)
        # 12. Canjear no baja de nivel
        r = services.consultarNivel("C001")
        self.assertEqual((r["nivel"], r["puntosAcum"]), ("Oro", 6073))

    def test_cliente_nuevo_es_bronce(self):
        services.creacionCliente("C001", "Marta Ruiz", "marta@correo.com", "01-02-2026")
        self.assertNivel("C001", "Bronce", 0, "1000")

    def test_umbral_de_plata_se_alcanza_en_1000_exactos(self):
        services.creacionCliente("C001", "Marta Ruiz", "marta@correo.com", "01-02-2026")
        services.registroCompras("C001", "9990.00", "01-02-2026")
        self.assertNivel("C001", "Bronce", 999, "1")
        services.registroCompras("C001", "10.00", "02-02-2026")
        self.assertNivel("C001", "Plata", 1000, "4000")

    def test_umbral_de_oro_se_alcanza_en_5000_exactos(self):
        services.creacionCliente("C001", "Marta Ruiz", "marta@correo.com", "01-02-2026")
        # 9990 -> 999 (Bronce), 10 -> 1 (1000, Plata), luego 3999 puntos con x1.25 dejan 4999
        services.registroCompras("C001", "9990.00", "01-02-2026")
        services.registroCompras("C001", "10.00", "02-02-2026")
        services.registroCompras("C001", "31992.00", "03-02-2026")
        self.assertNivel("C001", "Plata", 4999, "1")
        services.registroCompras("C001", "7.00", "04-02-2026")
        self.assertNivel("C001", "Plata", 4999, "1")
        services.registroCompras("C001", "10.00", "05-02-2026")
        self.assertNivel("C001", "Oro", 5000, "Ya estas en el nivel maximo")

    def test_nivel_de_cada_cliente_es_independiente(self):
        services.creacionCliente("C001", "Ana Pérez", "ana@correo.com", "01-02-2026")
        services.creacionCliente("C002", "Luis Gómez", "luis@correo.com", "01-02-2026")
        services.registroCompras("C001", "10000.00", "02-02-2026")
        self.assertNivel("C001", "Plata", 1000, "4000")
        self.assertNivel("C002", "Bronce", 0, "1000")
        self.assertCompra(services.registroCompras("C002", "100.00", "03-02-2026"), "C-2", 10, 10, "Bronce", "1.00")

    def test_canjear_no_reduce_puntos_acumulados_ni_nivel(self):
        services.creacionCliente("C001", "Marta Ruiz", "marta@correo.com", "01-02-2026")
        services.registroCompras("C001", "10000.00", "02-02-2026")
        services.canjearUnPremio("C001", "P03", "03-02-2026")
        self.assertEqual(services.consultarSaldo("C001"), 200)
        self.assertNivel("C001", "Plata", 1000, "4000")

    def test_compra_rechazada_no_cambia_el_nivel(self):
        services.creacionCliente("C001", "Marta Ruiz", "marta@correo.com", "01-02-2026")
        services.registroCompras("C001", "9000.00", "01-02-2026")
        self.assertCodigo("MONTO_INVALIDO", services.registroCompras, "C001", "-1000.00", "02-02-2026")
        self.assertCodigo("FECHA_INVALIDA", services.registroCompras, "C001", "1000.00", "30-02-2026")
        self.assertNivel("C001", "Bronce", 900, "100")

    def test_consultar_nivel_cliente_inexistente(self):
        self.assertCodigo("CLIENTE_NO_ENCONTRADO", services.consultarNivel, "C999")


class TestPrueba4Historial(PruebaBase):
    def test_canjes_sucesivos_e_historial(self):
        # 1 y 2. Cliente con 8000 puntos
        services.creacionCliente("C001", "Jorge Mora", "jorge@correo.com", "01-03-2026")
        services.registroCompras("C001", "80000.00", "02-03-2026")
        # 3 y 4. Dos canjes de P05
        services.canjearUnPremio("C001", "P05", "03-03-2026")
        services.canjearUnPremio("C001", "P05", "04-03-2026")
        # 5. El tercero falla
        self.assertCodigo("SALDO_INSUFICIENTE", services.canjearUnPremio, "C001", "P05", "05-03-2026")
        # 6. El canje fallido no cambió nada
        self.assertEqual(services.consultarSaldo("C001"), 0)
        # 7. Historial: tres movimientos en orden
        h = services.consultarHistorial("C001")
        self.assertEqual(len(h), 3)
        self.assertEqual((h[0]["tipo"], h[0]["puntos"], h[0]["fecha"], h[0]["referencia"]), ("ACUMULACION", 8000, date(2026, 3, 2), "C-1"))
        self.assertEqual((h[1]["tipo"], h[1]["puntos"], h[1]["fecha"], h[1]["referencia"]), ("CANJE", -4000, date(2026, 3, 3), "P-1"))
        self.assertEqual((h[2]["tipo"], h[2]["puntos"], h[2]["fecha"], h[2]["referencia"]), ("CANJE", -4000, date(2026, 3, 4), "P-2"))
        self.assertHistorialCoincideConSaldo("C001")

    def test_historial_de_cliente_nuevo_esta_vacio(self):
        services.creacionCliente("C001", "Jorge Mora", "jorge@correo.com", "01-03-2026")
        self.assertEqual(services.consultarHistorial("C001"), [])

    def test_compra_con_cero_puntos_no_genera_movimiento(self):
        services.creacionCliente("C001", "Jorge Mora", "jorge@correo.com", "01-03-2026")
        r = services.registroCompras("C001", "9.99", "02-03-2026")
        self.assertEqual((r["id"], r["puntos"], r["saldo"]), ("C-1", 0, 0))
        self.assertEqual(services.consultarHistorial("C001"), [])

    def test_compra_con_cero_puntos_entre_otras_no_aparece(self):
        services.creacionCliente("C001", "Jorge Mora", "jorge@correo.com", "01-03-2026")
        services.registroCompras("C001", "500.00", "02-03-2026")
        services.registroCompras("C001", "9.99", "03-03-2026")
        services.registroCompras("C001", "100.00", "04-03-2026")
        h = services.consultarHistorial("C001")
        self.assertEqual([m["referencia"] for m in h], ["C-1", "C-3"])
        self.assertEqual([m["puntos"] for m in h], [50, 10])
        self.assertHistorialCoincideConSaldo("C001")

    def test_movimientos_de_la_misma_fecha_conservan_el_orden(self):
        services.creacionCliente("C001", "Jorge Mora", "jorge@correo.com", "01-03-2026")
        services.registroCompras("C001", "10000.00", "02-03-2026")
        services.canjearUnPremio("C001", "P01", "02-03-2026")
        services.registroCompras("C001", "100.00", "02-03-2026")
        services.canjearUnPremio("C001", "P02", "02-03-2026")
        h = services.consultarHistorial("C001")
        self.assertEqual([m["tipo"] for m in h], ["ACUMULACION", "CANJE", "ACUMULACION", "CANJE"])
        self.assertEqual([m["puntos"] for m in h], [1000, -100, 12, -250])
        self.assertHistorialCoincideConSaldo("C001")

    def test_historial_usa_los_puntos_con_multiplicador(self):
        services.creacionCliente("C001", "Marta Ruiz", "marta@correo.com", "01-02-2026")
        services.registroCompras("C001", "10000.00", "01-02-2026")
        services.registroCompras("C001", "38.00", "02-02-2026")
        h = services.consultarHistorial("C001")
        self.assertEqual([m["puntos"] for m in h], [1000, 4])
        self.assertHistorialCoincideConSaldo("C001")

    def test_canje_fallido_no_genera_movimiento(self):
        services.creacionCliente("C001", "Jorge Mora", "jorge@correo.com", "01-03-2026")
        services.registroCompras("C001", "500.00", "02-03-2026")
        self.assertCodigo("SALDO_INSUFICIENTE", services.canjearUnPremio, "C001", "P02", "03-03-2026")
        self.assertCodigo("PREMIO_NO_ENCONTRADO", services.canjearUnPremio, "C001", "P99", "03-03-2026")
        self.assertEqual(len(services.consultarHistorial("C001")), 1)
        self.assertHistorialCoincideConSaldo("C001")

    def test_consultar_historial_no_altera_el_estado(self):
        services.creacionCliente("C001", "Jorge Mora", "jorge@correo.com", "01-03-2026")
        services.registroCompras("C001", "500.00", "02-03-2026")
        primera = services.consultarHistorial("C001")
        primera.clear()
        segunda = services.consultarHistorial("C001")
        self.assertEqual(len(segunda), 1)
        self.assertEqual(services.consultarSaldo("C001"), 50)
        self.assertEqual(services.consultarHistorial("C001"), segunda)

    def test_consultar_historial_cliente_inexistente(self):
        self.assertCodigo("CLIENTE_NO_ENCONTRADO", services.consultarHistorial, "C999")

    def test_historial_aislado_entre_clientes(self):
        services.creacionCliente("C001", "Ana Pérez", "ana@correo.com", "01-03-2026")
        services.creacionCliente("C002", "Luis Gómez", "luis@correo.com", "01-03-2026")
        services.registroCompras("C001", "1000.00", "02-03-2026")
        services.registroCompras("C002", "500.00", "02-03-2026")
        services.canjearUnPremio("C001", "P01", "03-03-2026")
        h1 = services.consultarHistorial("C001")
        h2 = services.consultarHistorial("C002")
        self.assertEqual([m["puntos"] for m in h1], [100, -100])
        self.assertEqual([m["puntos"] for m in h2], [50])
        self.assertHistorialCoincideConSaldo("C001")
        self.assertHistorialCoincideConSaldo("C002")

    def test_suma_del_historial_coincide_siempre_con_el_saldo(self):
        services.creacionCliente("C001", "Marta Ruiz", "marta@correo.com", "01-02-2026")
        operaciones = [
            ("compra", "9000.00", "01-02-2026"),
            ("compra", "1000.00", "02-02-2026"),
            ("canje", "P01", "03-02-2026"),
            ("compra", "38.00", "04-02-2026"),
            ("compra", "9.99", "04-02-2026"),
            ("canje", "P02", "05-02-2026"),
            ("compra", "40000.00", "06-02-2026"),
            ("canje", "P03", "07-02-2026"),
            ("compra", "133.30", "08-02-2026"),
        ]
        for tipo, dato, fecha in operaciones:
            with self.subTest(operacion=(tipo, dato, fecha)):
                if tipo == "compra":
                    services.registroCompras("C001", dato, fecha)
                else:
                    services.canjearUnPremio("C001", dato, fecha)
                self.assertHistorialCoincideConSaldo("C001")


class TestPrueba5HistorialConErrores(PruebaBase):
    def setUp(self):
        super().setUp()
        services.creacionCliente("C001", "Sofía Rojas", "sofia@correo.com", "01-03-2026")

    def test_flujo_completo(self):
        # 2. Compra válida
        r = services.registroCompras("C001", "200.00", "10-03-2026")
        self.assertEqual((r["id"], r["puntos"], r["saldo"]), ("C-1", 20, 20))
        # 3, 4 y 5. Operaciones inválidas
        self.assertCodigo("FECHA_INVALIDA", services.registroCompras, "C001", "100.00", "05-03-2026")
        self.assertCodigo("FECHA_INVALIDA", services.registroCompras, "C001", "100.00", "30-02-2026")
        self.assertCodigo("MONTO_INVALIDO", services.registroCompras, "C001", "abc", "11-03-2026")
        # 7. Saldo sin cambios
        self.assertEqual(services.consultarSaldo("C001"), 20)
        # 8. Historial con un solo movimiento
        h = services.consultarHistorial("C001")
        self.assertEqual(len(h), 1)
        self.assertEqual((h[0]["tipo"], h[0]["puntos"], h[0]["fecha"], h[0]["referencia"]), ("ACUMULACION", 20, date(2026, 3, 10), "C-1"))


if __name__ == "__main__":
    unittest.main()