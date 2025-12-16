# main_app.py

# Importar la clase desde el otro archivo (módulo)
from lavadero import Lavadero  # [file:1]

def ejecutarSimulacion(lavadero: Lavadero, prelavado: bool, secado_mano: bool, encerado: bool):
    """
    Simula el proceso de lavado para un vehículo con las opciones dadas.

    :param lavadero: Instancia de Lavadero.
    :param prelavado: bool, True si se solicita prelavado a mano.
    :param secado_mano: bool, True si se solicita secado a mano.
    :param encerado: bool, True si se solicita encerado.
    """  # [file:1]
    print("--- INICIO: Prueba de Lavado con Opciones Personalizadas ---")
    print(f"Opciones solicitadas: [Prelavado: {prelavado}, Secado a mano: {secado_mano}, Encerado: {encerado}]")

    try:
        # Inicia el lavado usando la API interna del lavadero
        lavadero._hacer_lavado(prelavado, secado_mano, encerado)  # [file:3]

        print("\nCoche entra. Estado inicial:")
        lavadero.imprimir_estado()  # [file:3]

        # Avanza por las fases
        print("\nAVANZANDO FASE POR FASE:")
        pasos = 0
        while lavadero.ocupado and pasos < 20:  # [file:3]
            lavadero.avanzarFase()  # [file:3]
            print("-> Fase actual: ", end="")
            lavadero.imprimir_fase()  # [file:3]
            print()
            pasos += 1

        print("\n----------------------------------------")
        print("Lavado completo. Estado final:")
        lavadero.imprimir_estado()  # [file:3]
        print(f"Ingresos acumulados: {lavadero.ingresos:.2f} €")  # [file:3]
        print("----------------------------------------")

    except ValueError as e:
        print(f"ERROR DE ARGUMENTO: {e}")
    except RuntimeError as e:
        print(f"ERROR DE ESTADO: {e}")
    except Exception as e:
        print(f"ERROR INESPERADO: {e}")  # [file:1]

# Punto de entrada (main): Aquí pasamos los parámetros
if __name__ == "__main__":
    lavadero_global = Lavadero()  # Usamos una única instancia para acumular ingresos [file:1]

    # EJEMPLO 1: Lavado completo con prelavado, secado a mano, con encerado
    # Precio esperado: 5.00 + 1.50 + 1.00 + 1.20 = 8.70 €
    print("\n=======================================================")
    print("EJEMPLO 1: Prelavado (S), Secado a mano (S), Encerado (S)")
    ejecutarSimulacion(lavadero_global, prelavado=True, secado_mano=True, encerado=True)

    # EJEMPLO 2: Lavado rápido sin extras
    # Precio esperado: 5.00 €
    print("\n=======================================================")
    print("EJEMPLO 2: Sin extras (Prelavado: N, Secado a mano: N, Encerado: N)")
    ejecutarSimulacion(lavadero_global, prelavado=False, secado_mano=False, encerado=False)

    # EJEMPLO 3: Lavado con encerado, pero sin secado a mano (Debe lanzar ValueError)
    print("\n=======================================================")
    print("EJEMPLO 3: ERROR (Encerado S, Secado a mano N)")
    ejecutarSimulacion(lavadero_global, prelavado=False, secado_mano=False, encerado=True)

    # EJEMPLO 4: Lavado con prelavado a mano
    # Precio esperado: 5.00 + 1.50 = 6.50 €
    print("\n=======================================================")
    print("EJEMPLO 4: Prelavado (S), Secado a mano (N), Encerado (N)")
    ejecutarSimulacion(lavadero_global, prelavado=True, secado_mano=False, encerado=False)