# Documentación de Pruebas - API de Videos

Este documento detalla las pruebas realizadas para cada endpoint del API REST de videos.

## Herramientas Utilizadas
- pytest para pruebas automatizadas
- Flask Test Client para simulación de requests
- SQLite en memoria para base de datos de pruebas

## Pruebas por Endpoint

### 1. GET /api/videos (Listar Videos)

#### Prueba: Obtener lista paginada
```bash
curl http://localhost:5000/api/videos?page=1&per_page=10
```
**Resultado Esperado:**
- Status: 200 OK
- Respuesta contiene: items, page, per_page, total, pages
- Máximo 10 items por página

#### Prueba: Paginación - Segunda página
```bash
curl http://localhost:5000/api/videos?page=2&per_page=5
```
**Resultado Esperado:**
- Status: 200 OK
- page = 2
- per_page = 5
- Contiene los siguientes 5 items

### 2. GET /api/videos/{id} (Obtener Video)

#### Prueba: Obtener video existente
```bash
curl http://localhost:5000/api/videos/1
```
**Resultado Esperado:**
- Status: 200 OK
- Datos completos del video

#### Prueba: Video no existente
```bash
curl http://localhost:5000/api/videos/999
```
**Resultado Esperado:**
- Status: 404 Not Found
- Mensaje de error apropiado

### 3. PUT /api/videos/{id} (Crear Video)

#### Prueba: Crear nuevo video
```bash
curl -X PUT http://localhost:5000/api/videos/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "Tutorial Flask", "views": 0, "likes": 0}'
```
**Resultado Esperado:**
- Status: 201 Created
- Video creado con datos correctos

#### Prueba: Crear con ID existente
```bash
# Intentar crear video con ID que ya existe
curl -X PUT http://localhost:5000/api/videos/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "Otro Video", "views": 0, "likes": 0}'
```
**Resultado Esperado:**
- Status: 409 Conflict
- Mensaje de error por conflicto

### 4. PATCH /api/videos/{id} (Actualizar Video)

#### Prueba: Actualizar video existente
```bash
curl -X PATCH http://localhost:5000/api/videos/1 \
     -H "Content-Type: application/json" \
     -d '{"views": 100}'
```
**Resultado Esperado:**
- Status: 200 OK
- Solo el campo views actualizado
- Otros campos sin cambios

#### Prueba: Actualizar video no existente
```bash
curl -X PATCH http://localhost:5000/api/videos/999 \
     -H "Content-Type: application/json" \
     -d '{"views": 100}'
```
**Resultado Esperado:**
- Status: 404 Not Found
- Mensaje de error apropiado

### 5. DELETE /api/videos/{id} (Eliminar Video)

#### Prueba: Eliminar video existente
```bash
curl -X DELETE http://localhost:5000/api/videos/1
```
**Resultado Esperado:**
- Status: 204 No Content
- Video eliminado de la base de datos

#### Prueba: Eliminar video no existente
```bash
curl -X DELETE http://localhost:5000/api/videos/999
```
**Resultado Esperado:**
- Status: 404 Not Found
- Mensaje de error apropiado

## Validación de Datos

### Pruebas de Validación

1. **Campos Requeridos**
   - PUT sin nombre: 400 Bad Request
   - PUT sin views: 400 Bad Request
   - PUT sin likes: 400 Bad Request

2. **Validación de Tipos**
   - views como string: 400 Bad Request
   - likes como string: 400 Bad Request

3. **Valores Inválidos**
   - views negativo: 400 Bad Request
   - likes negativo: 400 Bad Request

## Pruebas de Integración

Las pruebas automatizadas en `tests/test_api.py` cubren:
1. Flujo completo CRUD
2. Manejo de errores
3. Paginación
4. Validación de datos
5. Conflictos de recursos

## Resultados

Todas las pruebas han sido ejecutadas exitosamente, verificando:
- Funcionalidad correcta de todos los endpoints
- Manejo apropiado de errores
- Validación de datos de entrada
- Paginación funcionando correctamente
- Respuestas HTTP apropiadas para cada situación