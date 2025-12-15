# lavadero.py
# Archivo corregido con todos los errores solucionados

class Lavadero:
    """
    Simula el estado y las operaciones de un túnel de lavado de coches.
    
    Esta clase implementa una máquina de estados que gestiona el ciclo completo
    de lavado de un vehículo, incluyendo diferentes fases y opciones personalizables.
    Cumple con los requisitos de estado, avance de fase y reglas de negocio.
    
    Atributos de clase (constantes de fase):
        FASE_INACTIVO: Lavadero libre, esperando cliente
        FASE_COBRANDO: Procesando pago
        FASE_PRELAVADO_MANO: Limpieza manual previa (opcional)
        FASE_ECHANDO_AGUA: Mojado inicial
        FASE_ENJABONANDO: Aplicación de jabón
        FASE_RODILLOS: Cepillado con rodillos
        FASE_SECADO_AUTOMATICO: Secado automático (sin opción secado manual)
        FASE_SECADO_MANO: Secado manual (opcional)
        FASE_ENCERADO: Encerado manual (requiere secado manual)
    """
    
    # Constantes de fase - Representan los estados del lavadero
    FASE_INACTIVO = 0          # Estado inicial, lavadero libre
    FASE_COBRANDO = 1          # Procesando el pago
    FASE_PRELAVADO_MANO = 2    # Prelavado manual (si se solicita)
    FASE_ECHANDO_AGUA = 3      # Mojado inicial del vehículo
    FASE_ENJABONANDO = 4       # Aplicación de jabón
    FASE_RODILLOS = 5          # Cepillado con rodillos automáticos
    FASE_SECADO_AUTOMATICO = 6 # Secado automático (rápido)
    FASE_SECADO_MANO = 7       # Secado manual (más cuidadoso)
    FASE_ENCERADO = 8          # Encerado manual (protección extra)
    
    def __init__(self):
        """
        Constructor de la clase Lavadero.
        
        Inicializa el lavadero en estado inactivo con valores por defecto.
        Cumple con el Requisito 1: estado inicial correcto.
        
        Estado inicial:
            - Ingresos: 0.0€
            - Fase: INACTIVO (0)
            - Ocupado: False
            - Todas las opciones de lavado: False
        """
        # Atributos privados (encapsulación)
        self.__ingresos = 0.0                 # Ingresos acumulados
        self.__fase = self.FASE_INACTIVO      # Fase actual del lavadero
        self.__ocupado = False                # Indica si hay un lavado en curso
        self.__prelavado_a_mano = False       # Opción: prelavado manual
        self.__secado_a_mano = False          # Opción: secado manual
        self.__encerado = False               # Opción: encerado
        self.terminar()                       # Asegura estado inicial consistente
    
    # Properties (getters) - Acceso controlado a atributos privados
    @property
    def fase(self):
        """Devuelve la fase actual del lavadero (0-8)"""
        return self.__fase
    
    @property
    def ingresos(self):
        """Devuelve los ingresos acumulados del lavadero"""
        return self.__ingresos
    
    @property
    def ocupado(self):
        """Indica si el lavadero está ocupado (lavado en curso)"""
        return self.__ocupado
    
    @property
    def prelavado_a_mano(self):
        """Indica si el lavado actual incluye prelavado manual"""
        return self.__prelavado_a_mano
    
    @property
    def secado_a_mano(self):
        """Indica si el lavado actual incluye secado manual"""
        return self.__secado_a_mano
    
    @property
    def encerado(self):
        """Indica si el lavado actual incluye encerado"""
        return self.__encerado
    
    def terminar(self):
        """
        Resetea el lavadero al estado inactivo.
        
        Este método se llama cuando un ciclo de lavado termina.
        Resetea el estado pero MANTIENE los ingresos acumulados.
        """
        self.__fase = self.FASE_INACTIVO
        self.__ocupado = False
        self.__prelavado_a_mano = False
        self.__secado_a_mano = False
        self.__encerado = False
    
    def hacerLavado(self, prelavado_a_mano, secado_a_mano, encerado):
        """
        Inicia un nuevo ciclo de lavado con las opciones especificadas.
        
        Valida las reglas de negocio antes de iniciar el lavado:
        - Requisito 2: No se puede encerar sin secado manual
        - Requisito 3: No se puede iniciar un lavado si otro está en curso
        
        Args:
            prelavado_a_mano (bool): True para incluir prelavado manual
            secado_a_mano (bool): True para incluir secado manual
            encerado (bool): True para incluir encerado
        
        Raises:
            RuntimeError: Si el lavadero está ocupado (Requisito 3)
            ValueError: Si se intenta encerar sin secado manual (Requisito 2)
        """
        # Validación 1: Verificar que el lavadero no esté ocupado
        if self.__ocupado:
            raise RuntimeError(
                "No se puede iniciar un nuevo lavado mientras el lavadero está ocupado"
            )
        
        # Validación 2: No se puede encerar sin secado manual
        # El encerado requiere que primero se seque a mano para mejor acabado
        if not secado_a_mano and encerado:
            raise ValueError(
                "No se puede encerar el coche sin secado a mano"
            )
        
        # Inicializar el lavado
        self.__fase = self.FASE_INACTIVO  # Empieza en fase 0
        self.__ocupado = True              # Marca el lavadero como ocupado
        self.__prelavado_a_mano = prelavado_a_mano
        self.__secado_a_mano = secado_a_mano
        self.__encerado = encerado
    
    def _cobrar(self):
        """
        Calcula y añade los ingresos según las opciones seleccionadas.
        
        Tabla de precios (Requisitos 4-8):
        - Lavado base:          5.00€
        - Prelavado a mano:    +1.50€
        - Secado a mano:       +1.00€  
        - Encerado:            +1.20€
        
        Ejemplos:
        - Solo prelavado:                5.00 + 1.50 = 6.50€ (Req. 4)
        - Solo secado:                   5.00 + 1.00 = 6.00€ (Req. 5)
        - Secado + encerado:             5.00 + 1.00 + 1.20 = 7.20€ (Req. 6)
        - Prelavado + secado:            5.00 + 1.50 + 1.00 = 7.50€ (Req. 7)
        - Prelavado + secado + encerado: 5.00 + 1.50 + 1.00 + 1.20 = 8.70€ (Req. 8)
        
        Returns:
            float: El coste total del lavado
        """
        coste_lavado = 5.00  # Precio base del lavado
        
        # Añadir extras según opciones seleccionadas
        if self.__prelavado_a_mano:
            coste_lavado += 1.50  # Extra por prelavado manual
        
        if self.__secado_a_mano:
            coste_lavado += 1.00  # Extra por secado manual
        
        if self.__encerado:
            coste_lavado += 1.20  # Extra por encerado
        
        # Acumular ingresos
        self.__ingresos += coste_lavado
        return coste_lavadoº
    
    def avanzarFase(self):
        """
        Avanza el lavadero a la siguiente fase según el estado actual.
        
        Implementa la máquina de estados del lavadero.
        Las transiciones dependen de las opciones seleccionadas:
        - Con prelavado: incluye FASE_PRELAVADO_MANO (2)
        - Con secado manual: va a FASE_SECADO_MANO (7) en vez de AUTOMATICO (6)
        - Con encerado: añade FASE_ENCERADO (8) después de secado manual
        
        Requisitos de flujo (9-14):
        - Sin extras:                    0 → 1 → 3 → 4 → 5 → 6 → 0
        - Con prelavado:                 0 → 1 → 2 → 3 → 4 → 5 → 6 → 0
        - Con secado manual:             0 → 1 → 3 → 4 → 5 → 7 → 0
        - Secado + encerado:             0 → 1 → 3 → 4 → 5 → 7 → 8 → 0
        - Prelavado + secado:            0 → 1 → 2 → 3 → 4 → 5 → 7 → 0
        - Prelavado + secado + encerado: 0 → 1 → 2 → 3 → 4 → 5 → 7 → 8 → 0
        """
        # Si el lavadero no está ocupado, no hay nada que avanzar
        if not self.__ocupado:
            return
        
        # Máquina de estados - Transiciones según fase actual
        if self.__fase == self.FASE_INACTIVO:
            # De INACTIVO (0) → COBRANDO (1)
            coste_cobrado = self._cobrar()  # Procesar pago
            self.__fase = self.FASE_COBRANDO
            print(f" (COBRADO: {coste_cobrado:.2f} €) ", end="")
        
        elif self.__fase == self.FASE_COBRANDO:
            # De COBRANDO (1) → PRELAVADO_MANO (2) o ECHANDO_AGUA (3)
            if self.__prelavado_a_mano:
                self.__fase = self.FASE_PRELAVADO_MANO
            else:
                self.__fase = self.FASE_ECHANDO_AGUA
        
        elif self.__fase == self.FASE_PRELAVADO_MANO:
            # De PRELAVADO_MANO (2) → ECHANDO_AGUA (3)
            self.__fase = self.FASE_ECHANDO_AGUA
        
        elif self.__fase == self.FASE_ECHANDO_AGUA:
            # De ECHANDO_AGUA (3) → ENJABONANDO (4)
            self.__fase = self.FASE_ENJABONANDO
        
        elif self.__fase == self.FASE_ENJABONANDO:
            # De ENJABONANDO (4) → RODILLOS (5)
            self.__fase = self.FASE_RODILLOS
        
        elif self.__fase == self.FASE_RODILLOS:
            # De RODILLOS (5) → SECADO_MANO (7) o SECADO_AUTOMATICO (6)
            # ✅ CORRECCIÓN ERROR #1: Lógica corregida
            if self.__secado_a_mano:
                self.__fase = self.FASE_SECADO_MANO  # Con secado manual → fase 7
            else:
                self.__fase = self.FASE_SECADO_AUTOMATICO  # Sin secado manual → fase 6
        
        elif self.__fase == self.FASE_SECADO_AUTOMATICO:
            # De SECADO_AUTOMATICO (6) → INACTIVO (0)
            # El lavado termina después del secado automático
            self.terminar()
        
        elif self.__fase == self.FASE_SECADO_MANO:
            # De SECADO_MANO (7) → ENCERADO (8) o INACTIVO (0)
            # ✅ CORRECCIÓN ERROR #2: Transición a encerado agregada
            if self.__encerado:
                self.__fase = self.FASE_ENCERADO  # Con encerado → fase 8
            else:
                self.terminar()  # Sin encerado → termina
        
        elif self.__fase == self.FASE_ENCERADO:
            # De ENCERADO (8) → INACTIVO (0)
            # El encerado es la última fase opcional
            self.terminar()
        
        else:
            # Estado inválido - esto no debería ocurrir
            raise RuntimeError(
                f"Estado no válido: Fase {self.__fase}. El lavadero va a estallar..."
            )
    
    def imprimir_fase(self):
        """
        Imprime la descripción de la fase actual del lavadero.
        
        Usado para debugging y visualización del estado.
        """
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
        print(fases_map.get(self.__fase, f"{self.__fase} - En estado no válido"), end="")
    
    def imprimir_estado(self):
        """
        Imprime el estado completo del lavadero.
        
        Muestra:
        - Ingresos acumulados
        - Estado de ocupación
        - Opciones activas
        - Fase actual
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
    
    # ✅ CORRECCIÓN ERROR #3: Función movida DENTRO de la clase
    def ejecutar_y_obtener_fases(self, prelavado, secado, encerado):
        """
        Ejecuta un ciclo completo de lavado y devuelve las fases visitadas.
        
        Esta función auxiliar es útil para pruebas unitarias.
        Permite verificar que el flujo de fases es correcto según los requisitos.
        
        Args:
            prelavado (bool): Incluir prelavado manual
            secado (bool): Incluir secado manual
            encerado (bool): Incluir encerado
        
        Returns:
            list: Lista de fases visitadas durante el ciclo [0, 1, ..., 0]
        
        Raises:
            Exception: Si se detecta un bucle infinito (más de 15 fases)
        """
        # ✅ CORRECCIÓN: Llama a hacerLavado (no _hacer_lavado)
        self.hacerLavado(prelavado, secado, encerado)
        fases_visitadas = [self.fase]  # Empezar con fase inicial
        
        # Avanzar por todas las fases hasta terminar
        while self.ocupado:
            # Protección contra bucles infinitos
            if len(fases_visitadas) > 15:
                raise Exception(
                    "Bucle infinito detectado en la simulación de fases."
                )
            self.avanzarFase()
            fases_visitadas.append(self.fase)
        
        return fases_visitadas
