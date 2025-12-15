# Implementación de Tests Unitarios

## Introducción

En este apartado se documentan las pruebas unitarias implementadas para validar el correcto funcionamiento de la aplicación del lavadero de coches.

## Framework de Testing Utilizado

Se ha utilizado **Unittest** (o Pytest) para implementar los 14 tests unitarios requeridos.

## Tests Implementados

### Test 1: Estado Inicial del Lavadero

**Descripción:** Verifica que al crear un lavadero, este no tiene ingresos, no está ocupado, está en fase 0 y todas las opciones están en false.

```python
# Aquí va el código del test 1
```

**Resultado:**
```
✓ Test pasado correctamente
```

---

### Test 2: Excepción - Encerado sin Secado

**Descripción:** Verifica que se lanza ValueError cuando se intenta hacer encerado sin secado manual.

```python
# Aquí va el código del test 2
```

**Resultado:**
```
✓ Test pasado correctamente
```

---

### Test 3: Excepción - Lavadero Ocupado

**Descripción:** Verifica que se lanza ValueError cuando se intenta iniciar un lavado mientras otro está en curso.

```python
# Aquí va el código del test 3
```

---

## Tests de Precios (Tests 4-8)

### Test 4: Precio con Prelavado Manual
**Precio esperado:** 6.50€

### Test 5: Precio con Secado Manual
**Precio esperado:** 6.00€

### Test 6: Precio con Secado + Encerado
**Precio esperado:** 7.20€

### Test 7: Precio con Prelavado + Secado
**Precio esperado:** 7.50€

### Test 8: Precio Completo (todas las opciones)
**Precio esperado:** 8.70€

---

## Tests de Flujo de Fases (Tests 9-14)

### Test 9: Flujo sin extras
**Fases esperadas:** 0 → 1 → 3 → 4 → 5 → 6 → 0

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

> **Nota:** Aquí debes documentar los errores que encontraste al ejecutar los tests

### Error 1: [Nombre del error]
**Descripción:**
<!-- Explica el error -->

**Solución:**
<!-- Explica cómo lo solucionaste -->

---

## Ejecución de Tests

### Comando utilizado:
```bash
PYTHONPATH=src python3 -m unittest discover -v tests/
```

### Resultado Final:

<!-- Aquí pega una captura de pantalla de la ejecución de todos los tests -->

![Ejecución de tests](../imagenes/tests-resultado.png)

---

## Conclusiones

Todos los tests han sido implementados correctamente y validan:
- Estado inicial del lavadero
- Validaciones de excepciones
- Cálculo correcto de precios
- Transiciones de fase según opciones seleccionadas
