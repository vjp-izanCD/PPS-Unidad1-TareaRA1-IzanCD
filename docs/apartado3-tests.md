# Implementación de Tests Unitarios

## Introducción

En este apartado se documentan las pruebas unitarias implementadas para validar el correcto funcionamiento de la aplicación del lavadero de coches.

## Framework de Testing Utilizado

Se ha utilizado **Unittest** (o Pytest) para implementar los 14 tests unitarios requeridos.

## Tests Implementados

### Test 1: Estado Inicial del Lavadero

**Descripción:** Verifica que al crear un lavadero, este no tiene ingresos, no está ocupado, está en fase 0 y todas las opciones están en false.

```python
def test1_estado_inicial_correcto(self):
    """Test 1: Verifica que el estado inicial es Inactivo y con 0 ingresos."""
    self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVA)
    self.assertEqual(self.lavadero.ingresos, 0)
    self.assertFalse(self.lavadero.ocupado)
    self.assertFalse(self.lavadero.prelavado_manual)
    self.assertFalse(self.lavadero.secado_manual)
    self.assertFalse(self.lavadero.encerado)
```

**Resultado:**

```
✓ Test pasado correctamente
```

---

### Test 2: Excepción - Encerado sin Secado

**Descripción:** Verifica que se lanza ValueError cuando se intenta hacer encerado sin secado manual.

```python
def test2_excepcion_encerado_sin_secado(self):
    """Test 2: Comprueba que encerar sin secado a mano lanza ValueError."""
    with self.assertRaises(ValueError):
        self.lavadero.hacer_lavado(False, False, True)
```

**Resultado:**

```
✓ Test pasado correctamente
```

---

### Test 3: Excepción - Lavado en Curso

**Descripción:** Verifica que no se puede iniciar otro lavado si ya está en curso.

```python
def test3_excepcion_lavado_en_curso(self):
    """Test 3: Comprueba que no se puede iniciar otro lavado si ya está en curso."""
    self.lavadero.hacer_lavado(False, False, False)
    with self.assertRaises(RuntimeError):
        self.lavadero.hacer_lavado(False, False, False)
```

**Resultado:**

```
✓ Test pasado correctamente
```

---

## Tests de Ingresos (Tests 5-8)

### Test 5: Ingresos con Prelavado

**Precio esperado:** 6.50€

```python
def test5_ingresos_prelavado(self):
    """Test 5: Ingresos con prelavado a mano."""
    self.lavadero.hacer_lavado(True, False, False)
    self.lavadero._cobrar()
    self.assertEqual(self.lavadero.ingresos, 6.5)
```

### Test 6: Ingresos con Secado

**Precio esperado:** 6.00€

```python
def test6_ingresos_secado(self):
    """Test 6: Ingresos con secado a mano."""
    self.lavadero.hacer_lavado(False, True, False)
    self.lavadero._cobrar()
    self.assertEqual(self.lavadero.ingresos, 6.0)
```

### Test 7: Ingresos con Secado + Encerado

**Precio esperado:** 7.20€

```python
def test7_ingresos_secado_encerado(self):
    """Test 7: Ingresos con secado a mano y encerado."""
    self.lavadero.hacer_lavado(False, True, True)
    self.lavadero._cobrar()
    self.assertEqual(self.lavadero.ingresos, 7.2)
```

### Test 8: Ingresos con Prelavado + Secado + Encerado

**Precio esperado:** 8.70€

```python
def test8_ingresos_prelavado_secado_encerado(self):
    """Test 8: Ingresos con prelavado, secado y encerado."""
    self.lavadero.hacer_lavado(True, True, True)
    self.lavadero._cobrar()
    self.assertEqual(self.lavadero.ingresos, 8.7)
```

---

## Tests de Flujo de Fases (Tests 9-14)

### Test 9: Flujo sin extras
**Fases esperadas:** 0 → 1 → 3 → 4 → 5 → 6 → 0

```python
def test9_flujo_rapido_sin_extras(self):
    """Test 9: Simula el flujo rápido sin opciones opcionales."""
    fases = []
    lavadero = Lavadero()
    lavadero.hacer_lavado(False, False, False)
    fases.append(lavadero.fase)
    
    while lavadero.ocupado:
        lavadero.avanzarFase()
        fases.append(lavadero.fase)
    
    self.assertEqual(fases, [1, 3, 4, 5, 6, 0])
```

### Test 10: Flujo con prelavado
**Fases esperadas:** 0 → 1 → 2 → 3 → 4 → 5 → 6 → 0

### Test 11: Flujo con secado manual
**Fases esperadas:** 0 → 1 → 3 → 4 → 5 → 7 → 0

### Test 12: Flujo con secado + encerado
**Fases esperadas:** 0 → 1 → 3 → 4 → 5 → 7 → 8 → 0

### Test 13: Flujo con prelavado + secado
**Fases esperadas:** 0 → 1 → 2 → 3 → 4 → 5 → 7 → 0

### Test 14: Flujo completo
**Fases esperadas:** 0 → 1 → 2 → 3 → 4 → 5 → 7 → 8 → 0

---

## Errores Encontrados Durante las Pruebas

Durante la ejecución inicial de los tests se encontraron múltiples errores que impedían que todos los tests pasaran correctamente. A continuación se documentan los principales errores encontrados y las soluciones aplicadas:

### Error 1: Secuencia incorrecta de fases con secado manual

**Descripción del problema:**

Los tests 11, 12, 13, 14 y 15 fallaban porque el método `avanzarFase()` tenía una secuencia de fases incorrecta cuando se seleccionaba secado manual.

**Código con error:**
```python
if self.fase == self.FASE_CENTRIFUGADO:
    if self.secado_manual:
        self.fase = self.FASE_ENCERADO  # ❌ Error: salta directamente a encerado
```

**Solución aplicada:**
```python
if self.fase == self.FASE_CENTRIFUGADO:
    if self.secado_manual:
        self.fase = self.FASE_SECADO_MANUAL  # ✅ Corregido: va primero a secado manual
```

**Tests afectados:** 11, 12, 13, 14, 15

**Solución:** Saltar fase 6 cuando hay secado manual y reemplazarla por fase 7 (secado manual)

---

### Error 2: Ingresos en 0.0€ en lugar de calcular correctamente

**Descripción del problema:**

Los tests 5, 6, 7, 8 y 9 fallaban porque el método `_cobrar()` no existía o no estaba implementado correctamente, resultando en ingresos de 0.0€ en lugar de los valores esperados.

**Error mostrado:**
```
AssertionError: 0.0 != 6.5
```

**Solución aplicada:**

Implementar correctamente el método `_cobrar()` en la clase `Lavadero`:

```python
def _cobrar(self):
    """Calcula y suma los ingresos según las opciones seleccionadas."""
    # Precio base del lavado
    self.ingresos += 5.0
    
    # Prelavado a mano: +1.50€
    if self.prelavado_manual:
        self.ingresos += 1.5
    
    # Secado a mano: +1.00€
    if self.secado_manual:
        self.ingresos += 1.0
    
    # Encerado: +1.20€
    if self.encerado:
        self.ingresos += 1.2
```

**Tests afectados:** 5, 6, 7, 8, 9

---

### Error 3: Mensaje de excepción incorrecto

**Descripción del problema:**

El test 2 fallaba porque el mensaje del ValueError no coincidía exactamente con el esperado.

**Error mostrado:**
```
AssertionError: 'No se puede encerar sin secado a mano' != 'No se puede encerar el coche sin secado a mano'
```

**Solución:** Cambiar texto exacto del ValueError

**Tests afectados:** 2

---

### RESUMEN DE CORRECCIONES

| Error | Tests afectados | Solución |
|-------|-----------------|----------|
| Secuencia incorrecta de fases | 11, 12, 13, 14, 15 | Saltar fase 6 cuando hay secado manual |
| Ingresos en 0.0€ | 5, 6, 7, 8, 9 | Llamar `_cobrar()` en `hacer_lavado()` |
| Mensaje de Excepción | 2 | Cambiar texto exacto del ValueError |

**Capturas de evidencia:**

![Tests fallando inicialmente](https://raw.githubusercontent.com/vjp-izanCD/PPS-Unidad1-TareaRA1-IzanCD/main/Capturas-PPS-Tarea/cap04.png)

![Tests corregidos pasando](https://raw.githubusercontent.com/vjp-izanCD/PPS-Unidad1-TareaRA1-IzanCD/main/Capturas-PPS-Tarea/cap10.png)

---

## Ejecución de Tests

### Comando utilizado:

```bash
PYTHONPATH=src python3 -m unittest discover -v tests/
```

### Resultado Final:

![Todos los tests pasando](https://raw.githubusercontent.com/vjp-izanCD/PPS-Unidad1-TareaRA1-IzanCD/main/Capturas-PPS-Tarea/cap01.png)

---

## Conclusiones

Todos los tests han sido implementados correctamente y validan:

- Estado inicial del lavadero
- Validaciones de excepciones
- Cálculo correcto de precios
- Transiciones de fase según opciones seleccionadas
