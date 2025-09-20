# 📓 Guía de Notebooks de Validación

Este directorio contiene una colección de Jupyter Notebooks diseñados para probar, validar y experimentar con funcionalidades clave de forma aislada antes de integrarlas en la aplicación principal.

## Metodología: Validar Antes de Implementar

El principio fundamental de estos notebooks es **reducir el riesgo y acelerar el desarrollo**. Interactuar con APIs externas o bases de datos puede ser propenso a errores (credenciales incorrectas, formatos de datos inesperados, problemas de red, etc.).

Al usar un notebook, podemos:
- Probar la conectividad y autenticación con servicios como Spotify y Supabase de forma interactiva.
- Inspeccionar las respuestas de la API en tiempo real y entender su estructura.
- Desarrollar y depurar la lógica de transformación de datos (por ejemplo, convertir una respuesta de la API de Spotify en una entidad de dominio Pydantic) en un entorno rápido y visual.
- Probar consultas a la base de datos sin necesidad de ejecutar toda la aplicación.

Una vez que una pieza de lógica funciona correctamente en un notebook, se puede mover con confianza al código fuente de la aplicación, adaptándola a la arquitectura del proyecto.

## Estructura de los Notebooks

Los notebooks están organizados en directorios que reflejan las fases de desarrollo:

- **`01-setup/`**: Notebooks para verificar que el entorno, las dependencias y las variables de entorno están configuradas correctamente.
- **`02-authentication/`**: Para probar los flujos de autenticación de Spotify y la conexión a Supabase.
- **`03-spotify-api/`**: Para interactuar con la API de Spotify (obtener perfil, canciones, etc.).
- **`04-supabase-crud/`**: Para probar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en las tablas de Supabase.
- **`05-data-validation/`**: Para experimentar con modelos Pydantic y transformaciones de datos.
- **`06-integration/`**: Notebooks que prueban un flujo de extremo a extremo, como una sincronización completa.

## Orden de Ejecución Sugerido

Para un desarrollo guiado, se recomienda ejecutar los notebooks en el siguiente orden para validar cada capa de la aplicación de forma incremental:

1.  `notebooks/01-setup/environment-test.ipynb`
2.  `notebooks/02-authentication/supabase-connection-test.ipynb`
3.  `notebooks/02-authentication/spotify-oauth-test.ipynb`
4.  `notebooks/03-spotify-api/get-saved-tracks.ipynb`
5.  `notebooks/04-supabase-crud/create-track.ipynb`
6.  `notebooks/06-integration/end-to-end-sync.ipynb`
