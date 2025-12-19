# lavadero.py
# Clase que simula el funcionamiento de un túnel de lavado de coches
# con diferentes fases, opciones de servicio y gestión de ingresos

class Lavadero:
    """
    Simula el estado y las operaciones de un túnel de lavado de coches.
    Gestiona fases de lavado, opciones de servicios adicionales e ingresos.
    """

    # ================== CONSTANTES DE FASE ==================
    # Identificadores únicos para cada fase del proceso de lavado
    FASE_INACTIVO = 0                    # Lavadero no está procesando un vehículo
    FASE_COBRANDO = 1                    # Se está realizando el cobro del servicio
    FASE_PRELAVADO_MANO = 2              # Prelavado manual del vehículo
    FASE_ECHANDO_AGUA = 3                # Aplicación inicial de agua al vehículo
    FASE_ENJABONANDO = 4                 # Aplicación de jabón y detergentes
    FASE_RODILLOS = 5                    # Paso del vehículo por los rodillos de limpieza
    FASE_SECADO_AUTOMATICO = 6           # Secado automático sin intervención manual
    FASE_SECADO_MANO = 7                 # Secado manual por personal
    FASE_ENCERADO = 8                    # Aplicación de cera/encerado al vehículo

    def __init__(self):
        """
        Constructor de la clase Lavadero.
        Inicializa todos los atributos privados al estado inicial:
        - ingresos: 0€ (no hay dinero acumulado)
        - fase: INACTIVO (lavadero en reposo)
        - ocupado: False (no hay vehículo procesándose)
        - opciones de servicio: todas False (no hay servicios adicionales)
        """
        self.__ingresos = 0.0                      # Dinero acumulado en euros
        self.__fase = self.FASE_INACTIVO          # Fase actual del proceso
        self.__ocupado = False                     # Indica si hay un vehículo en procesamiento
        self.__prelavado_a_mano = False           # Opción: prelavado manual
        self.__secado_a_mano = False              # Opción: secado manual
        self.__encerado = False                   # Opción: aplicar cera

    # ================== PROPERTIES (SOLO LECTURA) ==================
    # Propiedades que permiten acceder a los atributos privados de forma controlada
    # Sin permitir modificación directa desde fuera de la clase

    @property
    def fase(self):
        """Devuelve la fase actual del lavadero."""
        return self.__fase

    @property
    def ingresos(self):
        """Devuelve los ingresos acumulados en euros."""
        return self.__ingresos

    @property
    def ocupado(self):
        """Devuelve True si el lavadero está procesando un vehículo."""
        return self.__ocupado

    @property
    def prelavado_a_mano(self):
        """Devuelve True si se ha seleccionado prelavado manual."""
        return self.__prelavado_a_mano

    @property
    def secado_a_mano(self):
        """Devuelve True si se ha seleccionado secado manual."""
        return self.__secado_a_mano

    @property
    def encerado(self):
        """Devuelve True si se ha seleccionado encerado."""
        return self.__encerado

    # ================== CONTROL DE ESTADO ==================

    def terminar(self):
        """
        Resetea el estado del lavadero al modo inactivo.
        Se llama automáticamente cuando termina un ciclo de lavado.
        
        IMPORTANTE: No modifica los ingresos, que se acumulan entre ciclos.
        """
        self.__fase = self.FASE_INACTIVO          # Volver a fase inactiva
        self.__ocupado = False                    # Liberar el lavadero
        self.__prelavado_a_mano = False           # Resetear opciones
        self.__secado_a_mano = False
        self.__encerado = False

    # ================== INICIO DEL LAVADO ==================

    def hacer_lavado(self, prelavado_a_mano: bool, secado_a_mano: bool, encerado: bool):
        """
        Inicia un nuevo ciclo de lavado con las opciones especificadas.
        
        Valida dos reglas de negocio críticas:
        1. No se puede iniciar un lavado si ya hay uno en curso (ocupado=True)
           → Lanza ValueError: "Lavado en curso"
        
        2. No se puede encerar sin haber seleccionado secado manual
           (encerado=True pero secado_a_mano=False)
           → Lanza ValueError: "Encerado sin secado a mano no permitido"
        
        Si pasa las validaciones:
        - Configura las opciones del nuevo ciclo
        - Marca el lavadero como ocupado
        - Realiza el cobro (actualiza ingresos)
        
        Args:
            prelavado_a_mano (bool): Si True, incluye prelavado manual (+1.50€)
            secado_a_mano (bool): Si True, incluye secado manual (+1.00€)
            encerado (bool): Si True, incluye encerado (+1.20€)
        
        Raises:
            ValueError: Si el lavadero está ocupado o si intenta encerar sin secado
        """
        # VALIDACIÓN 1: Comprobar si ya hay un lavado en curso
        if self.__ocupado:
            raise ValueError("Lavado en curso")

        # VALIDACIÓN 2: Comprobar regla de negocio sobre encerado y secado
        # No se puede encerar si no hay secado manual
        if not secado_a_mano and encerado:
            raise ValueError("Encerado sin secado a mano no permitido")

        # CONFIGURAR EL NUEVO CICLO
        self.__fase = self.FASE_INACTIVO          # Comenzar en fase inactiva
        self.__ocupado = True                     # Marcar como ocupado
        self.__prelavado_a_mano = prelavado_a_mano    # Guardar opciones
        self.__secado_a_mano = secado_a_mano
        self.__encerado = encerado

        # COBRAR EL SERVICIO
        self._cobrar()

    # ================== COBRO ==================

    def _cobrar(self):
        """
        Calcula y añade los ingresos del lavado actual a los ingresos acumulados.
        
        Estructura de precios (base + opcionales):
        - Base: 5.00€
        - Prelavado a mano: +1.50€
        - Secado a mano: +1.00€
        - Encerado: +1.20€
        
        Ejemplos de precios finales:
        - Sin extras: 5.00€
        - Solo prelavado: 6.50€
        - Solo secado: 6.00€
        - Secado + encerado: 7.20€
        - Todo: 8.70€
        
        Returns:
            float: El coste del lavado actual (antes de añadirse a ingresos)
        """
        # Precio base del lavado automático
        coste_lavado = 5.00

        # Añadir opcionales según lo seleccionado
        if self.__prelavado_a_mano:
            coste_lavado += 1.50
        if self.__secado_a_mano:
            coste_lavado += 1.00
        if self.__encerado:
            coste_lavado += 1.20

        # Acumular ingresos (importante: los ingresos persisten entre ciclos)
        self.__ingresos += coste_lavado
        return coste_lavado

    # ================== AVANCE DE FASES ==================

    def avanzarFase(self):
        """
        Avanza una fase en el ciclo de lavado según las reglas de transición.
        
        El flujo de fases depende de las opciones seleccionadas:
        
        FLUJO GENERAL:
        - Comienza en INACTIVO (0) → COBRANDO (1)
        - Luego: ECHANDO_AGUA (3) → ENJABONANDO (4) → RODILLOS (5)
        - Después depende de las opciones:
          * Sin secado manual: SECADO_AUTOMATICO (6) → INACTIVO (0)
          * Con secado manual: SECADO_MANO (7) → [ENCERADO (8) si seleccionado] → INACTIVO (0)
        
        FLUJOS POR OPCIÓN:
        1. Sin extras [0, 1, 3, 4, 5, 6, 0]
        2. Con prelavado [0, 1, 2, 3, 4, 5, 6, 0] (añade fase 2)
        3. Con secado [0, 1, 3, 4, 5, 7, 0] (salta a 7 en lugar de 6)
        4. Con secado + encerado [0, 1, 3, 4, 5, 7, 8, 0] (añade fase 8)
        
        Cuando se termina el ciclo, llama automáticamente a terminar() para resetear.
        """
        # Si no hay vehículo en procesamiento, no avanzar
        if not self.__ocupado:
            return

        # MÁQUINA DE ESTADOS: Transición según la fase actual
        if self.__fase == self.FASE_INACTIVO:
            # Inicio: pasar a cobrando (el cobro ya se hizo en hacer_lavado)
            self.__fase = self.FASE_COBRANDO

        elif self.__fase == self.FASE_COBRANDO:
            # Después de cobrar: ¿hay prelavado?
            if self.__prelavado_a_mano:
                self.__fase = self.FASE_PRELAVADO_MANO  # Sí: hacer prelavado
            else:
                self.__fase = self.FASE_ECHANDO_AGUA    # No: ir directamente al agua

        elif self.__fase == self.FASE_PRELAVADO_MANO:
            # Después del prelavado: ir al agua
            self.__fase = self.FASE_ECHANDO_AGUA

        elif self.__fase == self.FASE_ECHANDO_AGUA:
            # Después del agua: enjabonar
            self.__fase = self.FASE_ENJABONANDO

        elif self.__fase == self.FASE_ENJABONANDO:
            # Después de enjabonar: pasar rodillos
            self.__fase = self.FASE_RODILLOS

        elif self.__fase == self.FASE_RODILLOS:
            # Después de rodillos: ¿hay secado manual?
            if self.__secado_a_mano:
                self.__fase = self.FASE_SECADO_MANO    # Sí: secado a mano
            else:
                self.__fase = self.FASE_SECADO_AUTOMATICO  # No: secado automático

        elif self.__fase == self.FASE_SECADO_AUTOMATICO:
            # Secado automático es la última fase sin opcionales
            self.terminar()  # Finish: volver a inactivo

        elif self.__fase == self.FASE_SECADO_MANO:
            # Después del secado manual: ¿hay encerado?
            if self.__encerado:
                self.__fase = self.FASE_ENCERADO       # Sí: aplicar cera
            else:
                self.terminar()                        # No: fin del ciclo

        elif self.__fase == self.FASE_ENCERADO:
            # Encerado es la última fase
            self.terminar()  # Fin del ciclo

        else:
            # Estado inválido (nunca debería llegar aquí)
            raise RuntimeError(f"Estado no válido: Fase {self.__fase}. El lavadero va a estallar...")

    # ================== IMPRESIÓN (DEBUG) ==================

    def imprimir_fase(self):
        """
        Imprime el nombre descriptivo de la fase actual.
        Útil para depuración y visualización del estado.
        """
        # Diccionario que mapea números de fase a nombres descriptivos
        fases_map = {
            self.FASE_INACTIVO: "0 - Inactivo",
            self.FASE_COBRANDO: "1 - Cobrando",
            self.FASE_PRELAVADO_MANO: "2 - Haciendo prelavado a mano",
            self.FASE_ECHANDO_AGUA: "3 - Echándole agua",
            self.FASE_ENJABONANDO: "4 - Enjabonando",
            self.FASE_RODILLOS: "5 - Pasando rodillos",
            self.FASE_SECADO_AUTOMATICO: "6 - Haciendo secado automático",
            self.FASE_SECADO_MANO: "7 - Haciendo secado a mano",
            self.FASE_ENCERADO: "8 - Encerando a mano",
        }

        # Imprimir la descripción de la fase actual
        print(fases_map.get(self.__fase, f"{self.__fase} - En estado no válido"), end="")

    def imprimir_estado(self):
        """
        Imprime un resumen completo del estado actual del lavadero.
        Incluye ingresos, ocupación, opciones y fase actual.
        """
        print("----------------------------------------")
        print(f"Ingresos Acumulados: {self.ingresos:.2f} €")
        print(f"Ocupado: {self.ocupado}")
        print(f"Prelavado a mano: {self.prelavado_a_mano}")
        print(f"Secado a mano: {self.secado_a_mano}")
        print(f"Encerado: {self.encerado}")
        print("Fase: ", end="")
        self.imprimir_fase()
        print("\n----------------------------------------")

    # ================== FUNCIÓN PARA TESTS ==================

    def ejecutar_y_obtener_fases(self, prelavado, secado, encerado):
        """
        Ejecuta un ciclo completo de lavado y devuelve la lista de fases visitadas.
        
        Esta función es especialmente útil para tests unitarios que verifican
        que se sigue la secuencia de fases correcta.
        
        Args:
            prelavado (bool): Incluir prelavado manual
            secado (bool): Incluir secado manual
            encerado (bool): Incluir encerado
        
        Returns:
            list: Lista de identificadores de fase en el orden que se visitaron,
                  comenzando y terminando en FASE_INACTIVO (0)
        
        Ejemplo:
            fases = lavadero.ejecutar_y_obtener_fases(False, True, True)
            # Devuelve: [0, 1, 3, 4, 5, 7, 8, 0]
        """
        # Inicia el lavado mediante la API interna
        self.hacer_lavado(prelavado, secado, encerado)
        
        # Registrar la fase inicial (siempre INACTIVO)
        fases_visitadas = [self.fase]

        # Avanzar fase por fase hasta que el lavadero se libere
        while self.ocupado:
            # Límite de seguridad contra bucles infinitos (debería ser nunca)
            if len(fases_visitadas) > 20:
                raise Exception("Bucle infinito detectado en la simulación de fases.")
            
            # Avanzar una fase y registrar dónde estamos ahora
            self.avanzarFase()
            fases_visitadas.append(self.fase)

        # Devolver el recorrido completo de fases
        return fases_visitadas
