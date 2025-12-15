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
FASE_INACTIVO = 0      # Lavadero sin actividad
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
    self.fase = self.FASE_INACTIVO     # Fase actual del lavadero
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
    self.fase = self.FASE_INACTIVO
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

## Jupyter Notebook (Opcional)

> **Nota:** Si has realizado la actividad ElementosProgramaPython con Jupyter Notebook, puedes adjuntar el archivo `.ipynb` en esta sección.

<!-- Aquí puedes añadir el enlace o embed del Jupyter Notebook -->
