# Análisis y Documentación del Código Python

## Introducción

En este apartado se realiza un análisis detallado del código fuente de la aplicación `lavadero.py`, incluyendo comentarios explicativos sobre las clases, métodos, flujos de control y elementos de programación utilizados.

## Estructura del Código

### Clase Lavadero

La clase `Lavadero` implementa la lógica de un sistema de gestión de lavadero de coches que pasa por diferentes fases según las opciones seleccionadas.

#### Constantes de Fase

La clase define las siguientes constantes que representan las diferentes fases del proceso de lavado:

```python
# Constantes que definen las diferentes fases del proceso de lavado
FASE_INACTIVA = 0      # Lavadero sin actividad
FASE_INICIO = 1         # Fase inicial del lavado
FASE_PRELAVADO = 2      # Prelavado manual (opcional)
FASE_LAVADO = 3         # Lavado principal
FASE_ACLARADO = 4       # Aclarado del vehículo
FASE_CENTRIFUGADO = 5   # Centrifugado y eliminación de agua
FASE_SECADO_AUTO = 6    # Secado automático
FASE_SECADO_MANUAL = 7  # Secado manual (opcional)
FASE_ENCERADO = 8       # Encerado (opcional)
```

#### Atributos de Instancia

```python
def __init__(self):
    self.fase = self.FASE_INACTIVA     # Fase actual del lavadero
    self.ingresos = 0.0                 # Ingresos acumulados
    self.ocupado = False                # Estado de ocupación
    self.prelavado_manual = False       # Opción de prelavado manual
    self.secado_manual = False          # Opción de secado manual
    self.encerado = False               # Opción de encerado
```

### Métodos Principales

#### Método `_hacer_lavado()`

Este método privado gestiona el inicio de un lavado y calcula el precio según las opciones seleccionadas.

**Parámetros:**
- `prelavado`: Boolean - Indica si se solicita prelavado manual
- `secado`: Boolean - Indica si se solicita secado manual
- `encerado`: Boolean - Indica si se solicita encerado

**Validaciones:**
1. Verifica que el lavadero no esté ocupado
2. Valida que si se solicita encerado, también se solicite secado manual

**Cálculo de precios:**
- Lavado base: 5.00€
- Prelavado manual: +1.50€
- Secado manual: +1.00€
- Encerado: +1.20€ (requiere secado manual)

```python
def _hacer_lavado(self, prelavado, secado, encerado):
    # Validación: no se puede iniciar un lavado si ya hay uno en curso
    if self.ocupado:
        raise ValueError("El lavadero ya está ocupado")
    
    # Validación: el encerado requiere secado manual
    if encerado and not secado:
        raise ValueError("El encerado requiere secado manual")
    
    # Configuración de opciones
    self.prelavado_manual = prelavado
    self.secado_manual = secado
    self.encerado = encerado
    
    # Cálculo de ingresos según opciones seleccionadas
    precio = 5.00  # Precio base del lavado
    if prelavado:
        precio += 1.50
    if secado:
        precio += 1.00
    if encerado:
        precio += 1.20
    
    self.ingresos = precio
    self.ocupado = True
    self.fase = self.FASE_INICIO
```

#### Método `avanzarFase()`

Este método gestiona las transiciones entre las diferentes fases del proceso de lavado.

**Lógica de transiciones:**

```python
def avanzarFase(self):
    if not self.ocupado:
        return  # No hay lavado en curso
    
    # Transiciones desde cada fase
    if self.fase == self.FASE_INICIO:
        # Si hay prelavado manual, ir a fase 2, sino a fase 3
        if self.prelavado_manual:
            self.fase = self.FASE_PRELAVADO
        else:
            self.fase = self.FASE_LAVADO
    
    elif self.fase == self.FASE_PRELAVADO:
        # Después del prelavado, ir al lavado principal
        self.fase = self.FASE_LAVADO
    
    elif self.fase == self.FASE_LAVADO:
        # Después del lavado, ir al aclarado
        self.fase = self.FASE_ACLARADO
    
    elif self.fase == self.FASE_ACLARADO:
        # Después del aclarado, ir al centrifugado
        self.fase = self.FASE_CENTRIFUGADO
    
    elif self.fase == self.FASE_CENTRIFUGADO:
        # Decidir entre secado automático o manual
        if self.secado_manual:
            self.fase = self.FASE_SECADO_MANUAL
        else:
            self.fase = self.FASE_SECADO_AUTO
    
    elif self.fase == self.FASE_SECADO_AUTO:
        # Fin del proceso sin opciones adicionales
        self._finalizar_lavado()
    
    elif self.fase == self.FASE_SECADO_MANUAL:
        # Verificar si hay encerado
        if self.encerado:
            self.fase = self.FASE_ENCERADO
        else:
            self._finalizar_lavado()
    
    elif self.fase == self.FASE_ENCERADO:
        # Fin del proceso completo
        self._finalizar_lavado()
```

#### Método `_finalizar_lavado()`

Método privado que resetea el estado del lavadero al finalizar un ciclo.

```python
def _finalizar_lavado(self):
    # Resetear estado del lavadero
    self.fase = self.FASE_INACTIVA
    self.ocupado = False
    self.prelavado_manual = False
    self.secado_manual = False
    self.encerado = False
    # Los ingresos se mantienen acumulados
```

### Método Auxiliar para Tests

```python
def ejecutar_y_obtener_fases(self, prelavado, secado, encerado):
    """Ejecuta un ciclo completo y devuelve la lista de fases visitadas."""
    self._hacer_lavado(prelavado, secado, encerado)
    fases_visitadas = [self.fase]
    
    # Límite de seguridad para evitar bucles infinitos
    while self.ocupado:
        if len(fases_visitadas) > 15:
            raise Exception("Bucle infinito detectado")
        self.avanzarFase()
        fases_visitadas.append(self.fase)
    
    return fases_visitadas
```

## Diagrama de Flujo de Fases

### Flujo sin opciones extra:
```
0 → 1 → 3 → 4 → 5 → 6 → 0
```

### Flujo con prelavado manual:
```
0 → 1 → 2 → 3 → 4 → 5 → 6 → 0
```

### Flujo con secado manual:
```
0 → 1 → 3 → 4 → 5 → 7 → 0
```

### Flujo con secado manual y encerado:
```
0 → 1 → 3 → 4 → 5 → 7 → 8 → 0
```

### Flujo completo (todas las opciones):
```
0 → 1 → 2 → 3 → 4 → 5 → 7 → 8 → 0
```

## Manejo de Excepciones

La aplicación implementa dos validaciones principales mediante excepciones:

1. **ValueError por lavadero ocupado:**
   - Se lanza cuando se intenta iniciar un nuevo lavado mientras hay uno en curso
   - Mensaje: "El lavadero ya está ocupado"

2. **ValueError por encerado sin secado:**
   - Se lanza cuando se solicita encerado sin secado manual
   - Mensaje: "El encerado requiere secado manual"

## Conclusiones

El código implementa un sistema bien estructurado con:
- Uso adecuado de constantes para mejorar la legibilidad
- Métodos privados para encapsular la lógica interna
- Validaciones mediante excepciones
- Máquina de estados clara para las transiciones de fase
- Cálculo dinámico de precios según opciones

---

## Jupyter Notebook

[`Actividad-Elementos-Programa-Python`](https://raw.githubusercontent.com/vjp-izanCD/PPS-Unidad1-TareaRA1-IzanCD/main/docs/Actividad-Elementos-Programa-Python.ipynb)

# Normas
    Cuando se crea un lavadero, éste no tiene ingresos, no está ocupado, está en fase 0 y todas las opciones de lavado (prelavado a mano, secado a mano y encerado) están puestas a false.
    Cuando se intenta comprar un lavado con encerado pero sin secado a mano, se produce una IllegalArgumentException.
    Cuando se intenta hacer un lavado mientras que otro ya está en marcha, se produce una IllegalStateException.
    Si seleccionamos un lavado con prelavado a mano, los ingresos de lavadero son 6,50€.
    Si seleccionamos un lavado con secado a mano, los ingresos son 6,00€.
    Si seleccionamos un lavado con secado a mano y encerado, los ingresos son 7,20€.
    Si seleccionamos un lavado con prelavado a mano y secado a mano, los ingresos son 7,50€.
    Si seleccionamos un lavado con prelavado a mano, secado a mano y encerado, los ingresos son 8,70€.
    Si seleccionamos un lavado sin extras y vamos avanzando fases, el lavadero pasa por las fases 0, 1, 3, 4, 5, 6, 0.
    Si seleccionamos un lavado con prelavado a mano y vamos avanzando fases, el lavadero pasa por las fases 0, 1, 2, 3, 4, 5, 6, 0.
    Si seleccionamos un lavado con secado a mano y vamos avanzando fases, el lavadero pasa por las fases 0, 1, 3, 4, 5, 7, 0.12.
    Si seleccionamos un lavado con secado a mano y encerado y vamos avanzando fases, el lavadero pasa por las fases 0, 1, 3, 4, 5, 7, 8, 0.
    Si seleccionamos un lavado con prelavado a mano y secado a mano y vamos avanzando fases, el lavadero pasa por las fases 0, 1, 2, 3, 4, 5, 7, 0.
    Si seleccionamos un lavado con prelavado a mano, secado a mano y encerado y vamos avanzando fases, el lavadero pasa por las fases 0, 1, 2, 3, 4, 5, 7, 8, 0.


## Explicación de la clase Lavadero
La clase Lavadero simula un túnel de lavado de coches, gestionando el estado y las fases del proceso, así como los ingresos y servicios adicionales.


```python
# lavadero.py

class Lavadero:
```


      Cell In[9], line 3
        class Lavadero:
                       ^
    _IncompleteInputError: incomplete input
    


## Constantes de fases
Las constantes definen cada etapa por la que pasa el coche en el túnel de lavado. Cada número representa una fase diferente.


```python
    """
    Simula el estado y las operaciones de un túnel de lavado de coches.
    Cumple con los requisitos de estado, avance de fase y reglas de negocio.
    """

    FASE_INACTIVO = 0
    FASE_COBRANDO = 1
    FASE_PRELAVADO_MANO = 2
    FASE_ECHANDO_AGUA = 3
    FASE_ENJABONANDO = 4
    FASE_RODILLOS = 5
    FASE_SECADO_AUTOMATICO = 6
    FASE_SECADO_MANO = 7
    FASE_ENCERADO = 8
```

## Constructor y propiedades
El constructor inicializa los atributos privados y llama a terminar() para dejar el lavadero en estado inactivo. Las propiedades permiten acceder a los atributos de solo lectura desde fuera de la clase.


```python
    def __init__(self):
        """
        Constructor de la clase. Inicializa el lavadero.
        Cumple con el requisito 1.
        """
        self.__ingresos = 0.0
        self.__fase = self.FASE_INACTIVO
        self.__ocupado = False
        self.__prelavado_a_mano = False
        self.__secado_a_mano = False
        self.__encerado = False
        self.terminar() 

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
```

## Método terminar
Este método resetea el estado del lavadero, dejándolo como al inicio: inactivo y sin servicios activos.


```python
    def terminar(self):
        self.__fase = self.FASE_INACTIVO
        self.__ocupado = False
        self.__prelavado_a_mano = False
        self.__secado_a_mano = False
        self.__encerado = False
```

## Método hacerLavado
Inicia un nuevo ciclo de lavado. Valida que no haya otro coche y que no se intente encerar sin secado a mano. Luego configura las opciones seleccionadas.


```python
    def hacerLavado(self, prelavado_a_mano, secado_a_mano, encerado):
        """
        Inicia un nuevo ciclo de lavado, validando reglas de negocio.
        
        :raises RuntimeError: Si el lavadero está ocupado (Requisito 3).
        :raises ValueError: Si se intenta encerar sin secado a mano (Requisito 2).
        """
        if self.__ocupado:
            raise RuntimeError("No se puede iniciar un nuevo lavado mientras el lavadero está ocupado")
        
        if not secado_a_mano and encerado:
            raise ValueError("No se puede encerar el coche sin secado a mano")
        
        self.__fase = self.FASE_INACTIVO  
        self.__ocupado = True
        self.__prelavado_a_mano = prelavado_a_mano
        self.__secado_a_mano = secado_a_mano
        self.__encerado = encerado
```

## Método _cobrar
Calcula el precio del lavado según las opciones seleccionadas y actualiza los ingresos totales.


```python
    def _cobrar(self):
        """
        Calcula y añade los ingresos según las opciones seleccionadas (Requisitos 4-8).
        Precio base: 5.00€ (Implícito, 5.00€ de base + 1.50€ de prelavado + 1.00€ de secado + 1.20€ de encerado = 8.70€)
        """
        coste_lavado = 5.00
        
        if self.__prelavado_a_mano:
            coste_lavado += 1.50 
        
        if self.__secado_a_mano:
            coste_lavado += 1.20 
            
        if self.__encerado:
            coste_lavado += 1.00 
            
        self.__ingresos += coste_lavado
        return coste_lavado
```

## Método avanzarFase
Avanza el lavadero a la siguiente fase según la lógica de la máquina de estados. Siempre que el lavadero esté ocupado, pasa de una fase a la siguiente según las reglas de negocio.


```python
    def avanzarFase(self):
       
        if not self.__ocupado:
            return

        if self.__fase == self.FASE_INACTIVO:
            coste_cobrado = self._cobrar()
            self.__fase = self.FASE_COBRANDO
            print(f" (COBRADO: {coste_cobrado:.2f} €) ", end="")

        elif self.__fase == self.FASE_COBRANDO:
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
            if self.__secado_a_mano:
                self.__fase = self.FASE_SECADO_AUTOMATICO 

            else:
                self.__fase = self.FASE_SECADO_MANO
        
        elif self.__fase == self.FASE_SECADO_AUTOMATICO:
            self.terminar()
        
        elif self.__fase == self.FASE_SECADO_MANO:

            self.terminar() 
        
        elif self.__fase == self.FASE_ENCERADO:
            self.terminar() 
        
        else:
            raise RuntimeError(f"Estado no válido: Fase {self.__fase}. El lavadero va a estallar...")
```

## Métodos imprimir_fase e imprimir_estado
Estos métodos muestran información sobre la fase actual y el estado general del lavadero, útil para depuración y seguimiento.


```python
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
```

## Método ejecutar_y_obtener_fases
Simula un ciclo completo de lavado y devuelve la lista de fases visitadas, útil para pruebas unitarias y validación de la lógica.


```python
    # Esta función es útil para pruebas unitarias, no es parte del lavadero real
    # nos crea un array con las fases visitadas en un ciclo completo

    def ejecutar_y_obtener_fases(self, prelavado, secado, encerado):
        """Ejecuta un ciclo completo y devuelve la lista de fases visitadas."""
        self.lavadero.hacerLavado(prelavado, secado, encerado)
        fases_visitadas = [self.lavadero.fase]
        
        while self.lavadero.ocupado:
            # Usamos un límite de pasos para evitar bucles infinitos en caso de error
            if len(fases_visitadas) > 15:
                raise Exception("Bucle infinito detectado en la simulación de fases.")
            self.lavadero.avanzarFase()
            fases_visitadas.append(self.lavadero.fase)
            
        return fases_visitadas
```