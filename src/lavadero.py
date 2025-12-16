# lavadero.py

class Lavadero:
    """
    Simula el estado y las operaciones de un túnel de lavado de coches.
    """

    # Constantes de fase
    FASE_INACTIVO = 0
    FASE_COBRANDO = 1
    FASE_PRELAVADO_MANO = 2
    FASE_ECHANDO_AGUA = 3
    FASE_ENJABONANDO = 4
    FASE_RODILLOS = 5
    FASE_SECADO_AUTOMATICO = 6
    FASE_SECADO_MANO = 7
    FASE_ENCERADO = 8

    def __init__(self):
        """
        Constructor de la clase. Inicializa el lavadero.
        """
        self.__ingresos = 0.0
        self.__fase = self.FASE_INACTIVO
        self.__ocupado = False
        self.__prelavado_a_mano = False
        self.__secado_a_mano = False
        self.__encerado = False

    # ------------------------
    # PROPERTIES (solo lectura)
    # ------------------------
    @property
    def fase(self):
        return self.__fase

    @property
    def ingresos(self):
        return self.__ingresos

    @property
    def ocupado(self):
        return self.__ocupado

    @property
    def prelavado_a_mano(self):
        return self.__prelavado_a_mano

    @property
    def secado_a_mano(self):
        return self.__secado_a_mano

    @property
    def encerado(self):
        return self.__encerado

    # ------------------------
    # CONTROL DE ESTADO
    # ------------------------
    def terminar(self):
        """
        Resetea el estado del lavadero al modo inactivo,
        pero NO modifica los ingresos acumulados.
        """
        self.__fase = self.FASE_INACTIVO
        self.__ocupado = False
        self.__prelavado_a_mano = False
        self.__secado_a_mano = False
        self.__encerado = False

    # ------------------------
    # INICIO DEL LAVADO
    # ------------------------
    def hacer_lavado(self, prelavado_a_mano: bool, secado_a_mano: bool, encerado: bool):
        """
        Inicia un nuevo ciclo de lavado, validando reglas de negocio.
        - No se puede iniciar si está ocupado.
        - No se puede encerar sin haber elegido secado a mano.
        Además, los tests esperan que aquí ya se cobren los servicios.
        """
        # Test 3: si ya está ocupado -> ValueError("Lavado en curso")
        if self.__ocupado:
            raise ValueError("Lavado en curso")

        # Test 2: encerar sin secado a mano -> ValueError con este mensaje exacto
        if not secado_a_mano and encerado:
            raise ValueError("Encerado sin secado a mano no permitido")

        # Configuramos el nuevo ciclo
        self.__fase = self.FASE_INACTIVO
        self.__ocupado = True
        self.__prelavado_a_mano = prelavado_a_mano
        self.__secado_a_mano = secado_a_mano
        self.__encerado = encerado

        # Muy importante para los tests 5–9: que ingresos ya tenga el importe
        self._cobrar()

    # ------------------------
    # COBRO
    # ------------------------
    def _cobrar(self):
        """
        Calcula y añade los ingresos según las opciones seleccionadas.
        Precio base: 5.00 €
        + 1.50 € si hay prelavado a mano
        + 1.00 € si hay secado a mano
        + 1.20 € si hay encerado
        """
        coste_lavado = 5.00

        if self.__prelavado_a_mano:
            coste_lavado += 1.50
        if self.__secado_a_mano:
            coste_lavado += 1.00
        if self.__encerado:
            coste_lavado += 1.20

        self.__ingresos += coste_lavado
        return coste_lavado

    # ------------------------
    # AVANCE DE FASES
    # ------------------------
    def avanzarFase(self):
        """
        Avanza una fase en el ciclo de lavado según las reglas de negocio.
        Cuando se termina el ciclo, llama a terminar().
        """
        if not self.__ocupado:
            # Si no está ocupado, no hay nada que avanzar
            return

        if self.__fase == self.FASE_INACTIVO:
            # Ya se ha cobrado en hacer_lavado, así que solo pasamos a Cobrando
            self.__fase = self.FASE_COBRANDO

        elif self.__fase == self.FASE_COBRANDO:
            # Dependiendo del prelavado vamos a PRELAVADO o directamente a AGUA
            if self.__prelavado_a_mano:
                self.__fase = self.FASE_PRELAVADO_MANO
            else:
                self.__fase = self.FASE_ECHANDO_AGUA

        elif self.__fase == self.FASE_PRELAVADO_MANO:
            self.__fase = self.FASE_ECHANDO_AGUA

        elif self.__fase == self.FASE_ECHANDO_AGUA:
            self.__fase = self.FASE_ENJABONANDO

        elif self.__fase == self.FASE_ENJABONANDO:
            self.__fase = self.FASE_RODILLOS

        elif self.__fase == self.FASE_RODILLOS:
            # Lo que piden los tests:
            # - Sin secado mano: 5 -> 6 -> 0
            # - Con secado mano: 5 -> 7 -> (8 si encerado) -> 0
            if self.__secado_a_mano:
                self.__fase = self.FASE_SECADO_MANO
            else:
                self.__fase = self.FASE_SECADO_AUTOMATICO

        elif self.__fase == self.FASE_SECADO_AUTOMATICO:
            # Aquí nunca habrá secado_a_mano=True según los tests
            self.terminar()

        elif self.__fase == self.FASE_SECADO_MANO:
            if self.__encerado:
                self.__fase = self.FASE_ENCERADO
            else:
                self.terminar()

        elif self.__fase == self.FASE_ENCERADO:
            self.terminar()

        else:
            raise RuntimeError(f"Estado no válido: Fase {self.__fase}. El lavadero va a estallar...")

    # ------------------------
    # IMPRESIÓN (para debug)
    # ------------------------
    def imprimir_fase(self):
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
        print("----------------------------------------")
        print(f"Ingresos Acumulados: {self.ingresos:.2f} €")
        print(f"Ocupado: {self.ocupado}")
        print(f"Prelavado a mano: {self.prelavado_a_mano}")
        print(f"Secado a mano: {self.secado_a_mano}")
        print(f"Encerado: {self.encerado}")
        print("Fase: ", end="")
        self.imprimir_fase()
        print("\n----------------------------------------")

    # ------------------------
    # FUNCIÓN PARA TESTS
    # ------------------------
    def ejecutar_y_obtener_fases(self, prelavado, secado, encerado):
        """
        Ejecuta un ciclo completo y devuelve la lista de fases visitadas.
        Usada por los tests unitarios.
        """
        # Inicia el lavado mediante la API interna que usa el test
        self.hacer_lavado(prelavado, secado, encerado)
        fases_visitadas = [self.fase]

        # Avanzamos mientras el lavadero siga ocupado
        while self.ocupado:
            # Límite de seguridad contra bucles infinitos
            if len(fases_visitadas) > 20:
                raise Exception("Bucle infinito detectado en la simulación de fases.")
            self.avanzarFase()
            fases_visitadas.append(self.fase)

        return fases_visitadas