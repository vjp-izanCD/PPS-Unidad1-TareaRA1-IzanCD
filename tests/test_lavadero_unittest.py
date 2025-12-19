# test_lavadero.py
# Tests unitarios para validar el funcionamiento completo de la clase Lavadero
# Cubre todos los requisitos especificados en la tarea RA1

import unittest
from src.lavadero import Lavadero


class TestLavadero(unittest.TestCase):
    """
    Suite de pruebas unitarias para la clase Lavadero.
    Cada test verifica un requisito específico de la aplicación.
    """

    def setUp(self):
        """
        Método que se ejecuta antes de CADA test.
        Crea una instancia nueva y limpia de Lavadero.
        """
        self.lavadero = Lavadero()

    # ==================== REQUISITO 1 ====================
    def test01_estado_inicial_correcto(self):
        """
        TEST 1: Verificar que un lavadero recién creado está en estado inicial.
        
        Requisito: Cuando se crea un lavadero, éste no tiene ingresos, no está 
        ocupado, está en fase 0 y todas las opciones de lavado están False.
        
        Verificaciones:
        - ingresos = 0.0€
        - ocupado = False
        - fase = FASE_INACTIVO (0)
        - prelavado_a_mano = False
        - secado_a_mano = False
        - encerado = False
        """
        # Verificar que los ingresos comienzan en 0
        self.assertEqual(self.lavadero.ingresos, 0.0, "Ingresos iniciales deben ser 0€")
        
        # Verificar que no está ocupado
        self.assertFalse(self.lavadero.ocupado, "Lavadero inicial no debe estar ocupado")
        
        # Verificar que está en fase inactivo
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO, 
                        "Fase inicial debe ser INACTIVO (0)")
        
        # Verificar que todas las opciones están desactivadas
        self.assertFalse(self.lavadero.prelavado_a_mano, "Prelavado debe estar False")
        self.assertFalse(self.lavadero.secado_a_mano, "Secado debe estar False")
        self.assertFalse(self.lavadero.encerado, "Encerado debe estar False")

    # ==================== REQUISITO 2 ====================
    def test02_excepcion_encerado_sin_secado(self):
        """
        TEST 2: Verificar validación de regla de negocio.
        
        Requisito: Cuando se intenta comprar un lavado con encerado pero sin 
        secado a mano, se produce una ValueError (equivalente a IllegalArgumentException).
        
        Parámetros de lavado: (Prelavado: False, Secado: False, Encerado: True)
        Comportamiento esperado: ValueError con mensaje exacto
        """
        # Intentar crear un lavado inválido (encerado sin secado)
        # y verificar que lanza la excepción correcta
        with self.assertRaises(ValueError) as context:
            self.lavadero.hacer_lavado(False, False, True)
        
        # Verificar que el mensaje de error es exacto
        self.assertEqual(str(context.exception), "Encerado sin secado a mano no permitido",
                        "Mensaje de error debe ser exacto")

    # ==================== REQUISITO 3 ====================
    def test03_excepcion_lavado_en_curso(self):
        """
        TEST 3: Verificar que no se pueden iniciar dos lavados simultáneamente.
        
        Requisito: Cuando se intenta hacer un lavado mientras que otro ya está 
        en marcha, se produce una ValueError (equivalente a IllegalStateException).
        
        Proceso:
        1. Iniciar primer lavado (marca lavadero como ocupado)
        2. Intentar iniciar segundo lavado mientras el primero está en curso
        3. Verificar que lanza ValueError
        """
        # Iniciar primer lavado (esto deja el lavadero ocupado)
        self.lavadero.hacer_lavado(False, False, False)
        
        # Intentar iniciar otro lavado mientras está ocupado
        with self.assertRaises(ValueError) as context:
            self.lavadero.hacer_lavado(False, False, False)
        
        # Verificar mensaje exacto
        self.assertEqual(str(context.exception), "Lavado en curso",
                        "Debe indicar que hay lavado en curso")

    # ==================== REQUISITO 4 ====================
    def test04_ingresos_prelavado_solo(self):
        """
        TEST 4: Verificar cobro con prelavado a mano solamente.
        
        Requisito: Si seleccionamos un lavado con prelavado a mano, 
        los ingresos del lavadero son 6,50€.
        
        Desglose de precios:
        - Base: 5.00€
        - Prelavado: +1.50€
        - Total: 6.50€
        """
        # Crear lavado con prelavado pero sin secado ni encerado
        self.lavadero.hacer_lavado(True, False, False)
        
        # Verificar que los ingresos son exactamente 6.50€
        self.assertEqual(self.lavadero.ingresos, 6.50,
                        "Precio con prelavado debe ser 6.50€")

    # ==================== REQUISITO 5 ====================
    def test05_ingresos_secado_solo(self):
        """
        TEST 5: Verificar cobro con secado manual solamente.
        
        Requisito: Si seleccionamos un lavado con secado a mano, 
        los ingresos son 6,00€.
        
        Desglose de precios:
        - Base: 5.00€
        - Secado: +1.00€
        - Total: 6.00€
        """
        # Crear lavado con secado pero sin prelavado ni encerado
        self.lavadero.hacer_lavado(False, True, False)
        
        # Verificar que los ingresos son exactamente 6.00€
        self.assertEqual(self.lavadero.ingresos, 6.00,
                        "Precio con secado debe ser 6.00€")

    # ==================== REQUISITO 6 ====================
    def test06_ingresos_secado_encerado(self):
        """
        TEST 6: Verificar cobro con secado y encerado.
        
        Requisito: Si seleccionamos un lavado con secado a mano y encerado, 
        los ingresos son 7,20€.
        
        Desglose de precios:
        - Base: 5.00€
        - Secado: +1.00€
        - Encerado: +1.20€
        - Total: 7.20€
        """
        # Crear lavado con secado y encerado (pero sin prelavado)
        self.lavadero.hacer_lavado(False, True, True)
        
        # Verificar que los ingresos son exactamente 7.20€
        self.assertEqual(self.lavadero.ingresos, 7.20,
                        "Precio con secado y encerado debe ser 7.20€")

    # ==================== REQUISITO 7 ====================
    def test07_ingresos_prelavado_secado(self):
        """
        TEST 7: Verificar cobro con prelavado y secado.
        
        Requisito: Si seleccionamos un lavado con prelavado a mano y secado 
        a mano, los ingresos son 7,50€.
        
        Desglose de precios:
        - Base: 5.00€
        - Prelavado: +1.50€
        - Secado: +1.00€
        - Total: 7.50€
        """
        # Crear lavado con prelavado y secado (pero sin encerado)
        self.lavadero.hacer_lavado(True, True, False)
        
        # Verificar que los ingresos son exactamente 7.50€
        self.assertEqual(self.lavadero.ingresos, 7.50,
                        "Precio con prelavado y secado debe ser 7.50€")

    # ==================== REQUISITO 8 ====================
    def test08_ingresos_todo_completo(self):
        """
        TEST 8: Verificar cobro con todos los servicios (paquete completo).
        
        Requisito: Si seleccionamos un lavado con prelavado a mano, secado 
        a mano y encerado, los ingresos son 8,70€.
        
        Desglose de precios:
        - Base: 5.00€
        - Prelavado: +1.50€
        - Secado: +1.00€
        - Encerado: +1.20€
        - Total: 8.70€
        """
        # Crear lavado con todas las opciones activadas
        self.lavadero.hacer_lavado(True, True, True)
        
        # Verificar que los ingresos son exactamente 8.70€
        self.assertEqual(self.lavadero.ingresos, 8.70,
                        "Precio completo (todo) debe ser 8.70€")

    # ==================== REQUISITO 9 ====================
    def test09_flujo_sin_extras(self):
        """
        TEST 9: Verificar secuencia de fases para lavado sin extras.
        
        Requisito: Si seleccionamos un lavado sin extras y vamos avanzando 
        fases, el lavadero pasa por las fases 0, 1, 3, 4, 5, 6, 0.
        
        Explicación de flujo:
        0 (INACTIVO) → 1 (COBRANDO) → 3 (AGUA) → 4 (JABÓN) → 
        5 (RODILLOS) → 6 (SECADO AUTOMÁTICO) → 0 (INACTIVO)
        
        Nota: NO hay fase 2 (prelavado) ni 7/8 (secado/encerado manuales)
        """
        # Fases esperadas para lavado básico sin opcionales
        fases_esperadas = [0, 1, 3, 4, 5, 6, 0]
        
        # Ejecutar ciclo completo y obtener fases visitadas
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(
            prelavado=False,
            secado=False,
            encerado=False
        )
        
        # Verificar que la secuencia coincide exactamente
        self.assertEqual(fases_esperadas, fases_obtenidas,
                        f"Secuencia incorrecta.\nEsperado: {fases_esperadas}\nObtenido: {fases_obtenidas}")

    # ==================== REQUISITO 10 ====================
    def test10_flujo_con_prelavado(self):
        """
        TEST 10: Verificar secuencia de fases con prelavado a mano.
        
        Requisito: Si seleccionamos un lavado con prelavado a mano y vamos 
        avanzando fases, el lavadero pasa por las fases 0, 1, 2, 3, 4, 5, 6, 0.
        
        Explicación de flujo:
        0 (INACTIVO) → 1 (COBRANDO) → 2 (PRELAVADO MANO) → 3 (AGUA) → 
        4 (JABÓN) → 5 (RODILLOS) → 6 (SECADO AUTOMÁTICO) → 0 (INACTIVO)
        
        Diferencia con test 9: AÑADE fase 2 (prelavado manual)
        """
        # Fases esperadas: igual que sin extras pero añadiendo fase 2
        fases_esperadas = [0, 1, 2, 3, 4, 5, 6, 0]
        
        # Ejecutar ciclo con prelavado
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(
            prelavado=True,
            secado=False,
            encerado=False
        )
        
        # Verificar secuencia
        self.assertEqual(fases_obtenidas, fases_esperadas,
                        f"Secuencia incorrecta.\nEsperado: {fases_esperadas}\nObtenido: {fases_obtenidas}")

    # ==================== REQUISITO 11 ====================
    def test11_flujo_con_secado(self):
        """
        TEST 11: Verificar secuencia de fases con secado manual.
        
        Requisito: Si seleccionamos un lavado con secado a mano y vamos 
        avanzando fases, el lavadero pasa por las fases 0, 1, 3, 4, 5, 7, 0.
        
        Explicación de flujo:
        0 (INACTIVO) → 1 (COBRANDO) → 3 (AGUA) → 4 (JABÓN) → 
        5 (RODILLOS) → 7 (SECADO MANO) → 0 (INACTIVO)
        
        Diferencia con test 9: Salta de 5 a 7 (secado manual) en lugar de 6 (automático)
        """
        # Fases esperadas con secado manual
        fases_esperadas = [0, 1, 3, 4, 5, 7, 0]
        
        # Ejecutar ciclo con secado
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(
            prelavado=False,
            secado=True,
            encerado=False
        )
        
        # Verificar secuencia
        self.assertEqual(fases_obtenidas, fases_esperadas,
                        f"Secuencia incorrecta.\nEsperado: {fases_esperadas}\nObtenido: {fases_obtenidas}")

    # ==================== REQUISITO 12 ====================
    def test12_flujo_secado_encerado(self):
        """
        TEST 12: Verificar secuencia de fases con secado y encerado.
        
        Requisito: Si seleccionamos un lavado con secado a mano y encerado 
        y vamos avanzando fases, el lavadero pasa por las fases 0, 1, 3, 4, 5, 7, 8, 0.
        
        Explicación de flujo:
        0 (INACTIVO) → 1 (COBRANDO) → 3 (AGUA) → 4 (JABÓN) → 
        5 (RODILLOS) → 7 (SECADO MANO) → 8 (ENCERADO) → 0 (INACTIVO)
        
        Diferencia con test 11: AÑADE fase 8 (encerado) después del secado
        """
        # Fases esperadas: como test 11 pero añadiendo fase 8
        fases_esperadas = [0, 1, 3, 4, 5, 7, 8, 0]
        
        # Ejecutar ciclo con secado y encerado
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(
            prelavado=False,
            secado=True,
            encerado=True
        )
        
        # Verificar secuencia
        self.assertEqual(fases_obtenidas, fases_esperadas,
                        f"Secuencia incorrecta.\nEsperado: {fases_esperadas}\nObtenido: {fases_obtenidas}")

    # ==================== REQUISITO 13 ====================
    def test13_flujo_prelavado_secado(self):
        """
        TEST 13: Verificar secuencia con prelavado y secado.
        
        Requisito: Si seleccionamos un lavado con prelavado a mano y secado 
        a mano y vamos avanzando fases, el lavadero pasa por las fases 
        0, 1, 2, 3, 4, 5, 7, 0.
        
        Explicación de flujo:
        0 (INACTIVO) → 1 (COBRANDO) → 2 (PRELAVADO MANO) → 3 (AGUA) → 
        4 (JABÓN) → 5 (RODILLOS) → 7 (SECADO MANO) → 0 (INACTIVO)
        
        Diferencia: AÑADE fase 2 (prelavado) y SALTA a fase 7 (secado manual)
        """
        # Fases esperadas: prelavado (2) + secado manual (7)
        fases_esperadas = [0, 1, 2, 3, 4, 5, 7, 0]
        
        # Ejecutar ciclo con prelavado y secado
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(
            prelavado=True,
            secado=True,
            encerado=False
        )
        
        # Verificar secuencia
        self.assertEqual(fases_obtenidas, fases_esperadas,
                        f"Secuencia incorrecta.\nEsperado: {fases_esperadas}\nObtenido: {fases_obtenidas}")

    # ==================== REQUISITO 14 ====================
    def test14_flujo_completo_todas_opciones(self):
        """
        TEST 14: Verificar secuencia con TODAS las opciones activadas.
        
        Requisito: Si seleccionamos un lavado con prelavado a mano, secado 
        a mano y encerado y vamos avanzando fases, el lavadero pasa por las 
        fases 0, 1, 2, 3, 4, 5, 7, 8, 0.
        
        Explicación de flujo:
        0 (INACTIVO) → 1 (COBRANDO) → 2 (PRELAVADO MANO) → 3 (AGUA) → 
        4 (JABÓN) → 5 (RODILLOS) → 7 (SECADO MANO) → 8 (ENCERADO) → 0 (INACTIVO)
        
        Diferencia: Es la combinación de todos los extras
        """
        # Fases esperadas: combinación de prelavado (2) + secado (7) + encerado (8)
        fases_esperadas = [0, 1, 2, 3, 4, 5, 7, 8, 0]
        
        # Ejecutar ciclo con TODAS las opciones
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(
            prelavado=True,
            secado=True,
            encerado=True
        )
        
        # Verificar secuencia
        self.assertEqual(fases_obtenidas, fases_esperadas,
                        f"Secuencia incorrecta.\nEsperado: {fases_esperadas}\nObtenido: {fases_obtenidas}")


# ===================== EJECUCIÓN DE TESTS =====================
if __name__ == '__main__':
    """
    Punto de entrada para ejecutar los tests.
    Ejecutar desde terminal con: python -m unittest test_lavadero.py -v
    """
    unittest.main(verbosity=2)
