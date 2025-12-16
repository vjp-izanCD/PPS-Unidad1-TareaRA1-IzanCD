# tests/test_lavadero_unittest.py

import unittest
# Importamos la clase Lavadero desde el módulo padre
from src.lavadero import Lavadero

class TestLavadero(unittest.TestCase):
    
    # Método que se ejecuta antes de cada test.
    # Es el equivalente del @pytest.fixture en este contexto.
    def setUp(self):
        """Prepara una nueva instancia de Lavadero antes de cada prueba."""
        self.lavadero = Lavadero()

    # ----------------------------------------------------------------------    
    # Función para resetear el estado cuanto terminamos una ejecución de lavado
    # ----------------------------------------------------------------------
    def test_reseteo_estado_con_terminar(self):
        """Test 4: Verifica que terminar() resetea todas las flags y el estado."""
        self.lavadero.hacer_lavado(True, True, True)
        self.lavadero._cobrar()
        self.lavadero.terminar()
        
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertFalse(self.lavadero.ocupado)
        self.assertFalse(self.lavadero.prelavado_a_mano)
        # Los ingresos deben mantenerse
        self.assertTrue(self.lavadero.ingresos > 0)
        
    # ----------------------------------------------------------------------
    # TESTS  
    # ----------------------------------------------------------------------
        
    def test1_estado_inicial_correcto(self):
        """Test 1: Verifica que el estado inicial es Inactivo y con 0 ingresos."""
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertEqual(self.lavadero.ingresos, 0.0)
        self.assertFalse(self.lavadero.ocupado)
   
    def test2_excepcion_encerado_sin_secado(self):
        """Test 2: Comprueba que encerar sin secado a mano lanza ValueError."""
        # hacer_lavado: (Prelavado: False, Secado a mano: False, Encerado: True)
        with self.assertRaises(ValueError) as context:
            self.lavadero.hacer_lavado(False, False, True)
        self.assertEqual(str(context.exception), "Encerado sin secado a mano no permitido")

    def test3_excepcion_lavado_en_curso(self):
        """Test 3: Comprueba que no se puede iniciar otro lavado si ya está en curso."""
        self.lavadero.hacer_lavado(False, False, False)
        with self.assertRaises(ValueError) as context:
            self.lavadero.hacer_lavado(False, False, False)
        self.assertEqual(str(context.exception), "Lavado en curso")

    def test5_ingresos_prelavado(self):
        """Test 5: Ingresos con prelavado a mano."""
        self.lavadero.hacer_lavado(True, False, False)
        self.assertEqual(self.lavadero.ingresos, 6.50)

    def test6_ingresos_secado(self):
        """Test 6: Ingresos con secado a mano."""
        self.lavadero.hacer_lavado(False, True, False)
        self.assertEqual(self.lavadero.ingresos, 6.00)

    def test7_ingresos_secado_encerado(self):
        """Test 7: Ingresos con secado a mano y encerado."""
        self.lavadero.hacer_lavado(False, True, True)
        self.assertEqual(self.lavadero.ingresos, 7.20)

    def test8_ingresos_prelavado_secado(self):
        """Test 8: Ingresos con prelavado y secado a mano."""
        self.lavadero.hacer_lavado(True, True, False)
        self.assertEqual(self.lavadero.ingresos, 7.50)

    def test9_ingresos_prelavado_secado_encerado(self):
        """Test 9: Ingresos con prelavado, secado y encerado."""
        self.lavadero.hacer_lavado(True, True, True)
        self.assertEqual(self.lavadero.ingresos, 8.70)

    # ----------------------------------------------------------------------
    # Tests de flujo de fases
    # Utilizamos la función ejecutar_y_obtener_fases(self, prelavado, secado, encerado)
    # ----------------------------------------------------------------------
    def test10_flujo_rapido_sin_extras(self):
        """Test 10: Simula el flujo rápido sin opciones opcionales."""
        fases_esperadas = [0, 1, 3, 4, 5, 6, 0]
         
        # Ejecutar el ciclo completo y obtener las fases
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(
            prelavado=False,
            secado=False,
            encerado=False
        )
        
        # Verificar que las fases obtenidas coinciden con las esperadas
        self.assertEqual(
            fases_esperadas,
            fases_obtenidas,
            f"Secuencia de fases incorrecta.\nEsperadas: {fases_esperadas}\nObtenidas: {fases_obtenidas}"
        )

    def test11_flujo_prelavado(self):
        """Test 11: Simula el flujo con prelavado a mano."""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 6, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(prelavado=True, secado=False, encerado=False)
        self.assertEqual(fases_obtenidas, fases_esperadas, 
                        f"Secuencia de fases incorrecta.\nEsperadas: {fases_esperadas}\nObtenidas: {fases_obtenidas}")

    def test12_flujo_secado(self):
        """Test 12: Simula el flujo con secado a mano."""
        fases_esperadas = [0, 1, 3, 4, 5, 7, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(prelavado=False, secado=True, encerado=False)
        self.assertEqual(fases_obtenidas, fases_esperadas, 
                        f"Secuencia de fases incorrecta.\nEsperadas: {fases_esperadas}\nObtenidas: {fases_obtenidas}")

    def test13_flujo_secado_encerado(self):
        """Test 13: Simula el flujo con secado y encerado."""
        fases_esperadas = [0, 1, 3, 4, 5, 7, 8, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(prelavado=False, secado=True, encerado=True)
        self.assertEqual(fases_obtenidas, fases_esperadas, 
                        f"Secuencia de fases incorrecta.\nEsperadas: {fases_esperadas}\nObtenidas: {fases_obtenidas}")

    def test14_flujo_prelavado_secado(self):
        """Test 14: Simula el flujo con prelavado y secado a mano."""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 7, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(prelavado=True, secado=True, encerado=False)
        self.assertEqual(fases_obtenidas, fases_esperadas, 
                        f"Secuencia de fases incorrecta.\nEsperadas: {fases_esperadas}\nObtenidas: {fases_obtenidas}")

    def test15_flujo_prelavado_secado_encerado(self):
        """Test 15: Simula el flujo con prelavado, secado y encerado."""
        fases_esperadas = [0, 1, 2, 3, 4, 5, 7, 8, 0]
        fases_obtenidas = self.lavadero.ejecutar_y_obtener_fases(prelavado=True, secado=True, encerado=True)
        self.assertEqual(fases_obtenidas, fases_esperadas, 
                        f"Secuencia de fases incorrecta.\nEsperadas: {fases_esperadas}\nObtenidas: {fases_obtenidas}")

# Bloque de ejecución para ejecutar los tests si el archivo es corrido directamente
if __name__ == '__main__':
    unittest.main()
