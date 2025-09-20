# 🤖 Guía de Desarrollo Impulsado por IA

Este proyecto está diseñado para ser construido por un asistente de IA (LLM) con acceso a una CLI, siguiendo una metodología iterativa y basada en validación.

## 🔄 Flujo de Desarrollo Cíclico

El proceso de desarrollo para cada nueva funcionalidad debe seguir estos pasos:

1.  **Lectura y Comprensión**: El LLM debe leer la tarea y los documentos de arquitectura relevantes.
2.  **Validación Aislada (Notebook)**: Antes de escribir el código de producción, el LLM debe usar o crear un **Jupyter Notebook** para validar la funcionalidad clave de forma aislada. Por ejemplo, probar la conexión a la API de Spotify, transformar un objeto de datos, o verificar una consulta a Supabase.
3.  **Implementación (Código de Aplicación)**: Una vez que la lógica ha sido validada en el notebook, el LLM implementa la funcionalidad dentro de la estructura de la aplicación FastAPI, siguiendo los patrones de arquitectura definidos.
4.  **Pruebas (Unitarias/Integración)**: El LLM escribe las pruebas correspondientes para la nueva funcionalidad.
5.  **Iteración**: Se repite el ciclo para el siguiente hito.

Este enfoque reduce errores, asegura que las integraciones con APIs externas funcionan como se espera y permite un desarrollo incremental y robusto.

## 🎯 Hitos de Desarrollo del Proyecto

Esta es la hoja de ruta recomendada. Cada fase principal debe ser abordada en orden.

### Fase 1: Configuración y Estructura Base
- [ ] **Tarea 1.1**: Crear la estructura completa de directorios y archivos vacíos (`__init__.py`, etc.).
- [ ] **Tarea 1.2**: Llenar el archivo `pyproject.toml` y `requirements.txt` con todas las dependencias.
- [ ] **Tarea 1.3**: Implementar la carga de configuración en `src/infrastructure/config/settings.py` usando `pydantic-settings`.
- [ ] **Tarea 1.4**: Crear el archivo `main.py` básico con una instancia de FastAPI y un endpoint de prueba (`/`).

### Fase 2: Autenticación y Conexión
- [ ] **Tarea 2.1 (Validación)**: Usar `notebooks/02-authentication/spotify-oauth-test.ipynb` para completar y probar el flujo de autenticación OAuth2 con Spotify.
- [ ] **Tarea 2.2 (Implementación)**: Implementar la lógica de autenticación en `src/adapters/spotify/auth.py` y los endpoints correspondientes en `src/presentation/api/v1/auth.py`.
- [ ] **Tarea 2.3 (Validación)**: Usar `notebooks/02-authentication/supabase-connection-test.ipynb` para verificar la conexión con Supabase.
- [ ] **Tarea 2.4 (Implementación)**: Crear el cliente de Supabase en `src/adapters/supabase/client.py`.

### Fase 3: Lógica de Negocio Principal (Core)
- [ ] **Tarea 3.1**: Definir las entidades de dominio en `src/core/entities/`.
- [ ] **Tarea 3.2**: Definir las interfaces de los repositorios en `src/core/repositories/`.
- [ ] **Tarea 3.3 (Validación)**: Usar `notebooks/03-spotify-api/get-saved-tracks.ipynb` para obtener y transformar los datos de las canciones guardadas.
- [ ] **Tarea 3.4 (Implementación)**: Implementar el `SpotifyRepository` en `src/adapters/spotify/repository.py`.
- [ ] **Tarea 3.5 (Validación)**: Usar `notebooks/04-supabase-crud/create-track.ipynb` para insertar un registro en la tabla `saved_tracks`.
- [ ] **Tarea 3.6 (Implementación)**: Implementar el `SupabaseTrackRepository` en `src/adapters/supabase/repository.py`.
- [ ] **Tarea 3.7**: Implementar el `SyncService` en `src/core/services/sync_service.py`, que orquesta la sincronización.

### Fase 4: API REST y Endpoints
- [ ] **Tarea 4.1**: Definir los esquemas Pydantic para requests y responses en `src/presentation/schemas/`.
- [ ] **Tarea 4.2**: Implementar los endpoints para la sincronización y gestión de tracks en `src/presentation/api/v1/tracks.py`, usando inyección de dependencias.
- [ ] **Tarea 4.3**: Configurar la documentación de Swagger/OpenAPI con ejemplos y descripciones claras.

### Fase 5: Pruebas y Refinamiento
- [ ] **Tarea 5.1**: Escribir tests unitarios para los servicios del `core`.
- [ ] **Tarea 5.2**: Escribir tests de integración para los endpoints de la API.
- [ ] **Tarea 5.3**: Implementar logging y manejo de errores robusto en toda la aplicación.

## 🚨 Consideraciones Clave para el LLM
1.  **Validación Primero**: **No omitir el paso del notebook**. Es la forma más rápida de depurar problemas con APIs externas.
2.  **Pasos Pequeños**: Implementar una función o método a la vez. No intentes construir una clase o módulo completo de una sola vez.
3.  **Verificación Constante**: Después de cada cambio de código, ejecuta los tests o el servidor para asegurar que nada se ha roto.
4.  **Seguir la Arquitectura**: Adhiérete estrictamente a la separación de capas. La lógica de negocio no debe saber nada sobre FastAPI o Supabase.
