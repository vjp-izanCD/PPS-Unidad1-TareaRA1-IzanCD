# main_app.py
# Aplicación de demostración del funcionamiento del lavadero
# Ejecuta 4 ejemplos de uso mostrando distintas configuraciones de lavado

from lavadero import Lavadero


def ejecutarSimulacion(lavadero: Lavadero, prelavado: bool, secado_mano: bool, encerado: bool):
    """
    Simula el proceso completo de lavado para un vehículo con las opciones dadas.
    Muestra el estado inicial, avanza fase por fase y muestra el estado final.
    
    Args:
        lavadero (Lavadero): Instancia del lavadero a utilizar
        prelavado (bool): True si se solicita prelavado a mano
        secado_mano (bool): True si se solicita secado a mano
        encerado (bool): True si se solicita encerado
    """
    print("--- INICIO: Prueba de Lavado con Opciones Personalizadas ---")
    print(f"Opciones solicitadas: [Prelavado: {prelavado}, Secado a mano: {secado_mano}, Encerado: {encerado}]")
    print()

    try:
        # Inicia el proceso de lavado con la configuración especificada
        lavadero.hacer_lavado(prelavado, secado_mano, encerado)

        # Mostrar estado después del cobro
        print("Coche entra. Estado inicial (después de cobro):")
        lavadero.imprimir_estado()

        # Avanzar fase por fase hasta que termine
        print("\nAVANZANDO FASE POR FASE:")
        pasos = 0
        # Límite de seguridad para evitar bucles infinitos
        while lavadero.ocupado and pasos < 20:
            # Avanzar una fase
            lavadero.avanzarFase()
            
            # Mostrar en qué fase estamos ahora
            print("-> Fase actual: ", end="")
            lavadero.imprimir_fase()
            print()
            
            pasos += 1

        # Mostrar estado final después de completar el lavado
        print("\n----------------------------------------")
        print("✓ Lavado completo. Estado final:")
        lavadero.imprimir_estado()
        print(f"Ingresos acumulados: {lavadero.ingresos:.2f} €")
        print("----------------------------------------")

    except ValueError as e:
        # Capturar errores de validación (argumentos inválidos)
        print(f"❌ ERROR DE VALIDACIÓN: {e}")
    except RuntimeError as e:
        # Capturar errores de estado
        print(f"❌ ERROR DE ESTADO: {e}")
    except Exception as e:
        # Capturar cualquier otro error inesperado
        print(f"❌ ERROR INESPERADO: {e}")


# ===================== PUNTO DE ENTRADA (MAIN) =====================
if __name__ == "__main__":
    # Crear una única instancia de Lavadero que será reutilizada
    # Esto permite que los ingresos se acumulen entre ejemplos
    lavadero_global = Lavadero()

    # ==================== EJEMPLO 1 ====================
    # Lavado COMPLETO con todas las opciones
    # Precio esperado: 5.00 (base) + 1.50 (prelavado) + 1.00 (secado) + 1.20 (encerado) = 8.70 €
    print("\n" + "="*55)
    print("EJEMPLO 1: Prelavado (SÍ), Secado a mano (SÍ), Encerado (SÍ)")
    print("Precio esperado: 8.70 €")
    print("="*55)
    ejecutarSimulacion(lavadero_global, prelavado=True, secado_mano=True, encerado=True)

    # ==================== EJEMPLO 2 ====================
    # Lavado RÁPIDO sin ningún extra
    # Precio esperado: 5.00 € (solo base)
    print("\n" + "="*55)
    print("EJEMPLO 2: Lavado básico (Sin extras)")
    print("Precio esperado: 5.00 €")
    print("="*55)
    ejecutarSimulacion(lavadero_global, prelavado=False, secado_mano=False, encerado=False)

    # ==================== EJEMPLO 3 ====================
    # Lavado INVÁLIDO - Intentar encerar sin secado a mano
    # Este debe fallar porque viola la regla de negocio
    # Excepción esperada: ValueError("Encerado sin secado a mano no permitido")
    print("\n" + "="*55)
    print("EJEMPLO 3: CASO DE ERROR - Encerado sin Secado a mano")
    print("Comportamiento esperado: Lanzar ValueError")
    print("="*55)
    ejecutarSimulacion(lavadero_global, prelavado=False, secado_mano=False, encerado=True)

    # ==================== EJEMPLO 4 ====================
    # Lavado con SOLO prelavado a mano
    # Precio esperado: 5.00 (base) + 1.50 (prelavado) = 6.50 €
    print("\n" + "="*55)
    print("EJEMPLO 4: Prelavado (SÍ), Secado a mano (NO), Encerado (NO)")
    print("Precio esperado: 6.50 €")
    print("="*55)
    ejecutarSimulacion(lavadero_global, prelavado=True, secado_mano=False, encerado=False)

    # ==================== RESUMEN FINAL ====================
    print("\n" + "="*55)
    print("RESUMEN DE INGRESOS ACUMULADOS")
    print("="*55)
    print(f"Total de ingresos después de 4 intentos: {lavadero_global.ingresos:.2f} €")
    print()
    print("Desglose:")
    print("- Ejemplo 1 (Completo): +8.70 €")
    print("- Ejemplo 2 (Básico): +5.00 €")
    print("- Ejemplo 3 (Error): +0.00 € (no se ejecutó)")
    print("- Ejemplo 4 (Prelavado): +6.50 €")
    print(f"- Total esperado: {8.70 + 5.00 + 0.00 + 6.50:.2f} €")
    print("="*55)
