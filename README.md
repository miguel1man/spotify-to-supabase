# Spotify to Supabase Tracker

Una aplicación FastAPI para extraer y sincronizar las canciones guardadas de Spotify con una base de datos Supabase.

## 🚀 Descripción General

Este proyecto permite a un usuario autenticarse a través de Spotify, extraer todas sus canciones guardadas ("Me Gusta") y sincronizarlas en una base de datos PostgreSQL gestionada por Supabase. La interacción se realiza a través de una API RESTful construida con FastAPI.

El repositorio está especialmente estructurado para ser desarrollado de forma iterativa por un Asistente de IA con acceso a un entorno de línea de comandos (CLI).

## 🗺️ Guía del Proyecto

Para entender completamente el proyecto, la arquitectura y la hoja de ruta de desarrollo, consulta los siguientes documentos:

- **[🛠️ Configuración y Entorno](./docs/SETUP.md)**: Instrucciones detalladas sobre cómo configurar el entorno de desarrollo, gestionar dependencias e instalar las herramientas necesarias.
- **[🏗️ Arquitectura del Proyecto](./docs/ARCHITECTURE.md)**: Una explicación en profundidad de la arquitectura hexagonal, la estructura de directorios y los patrones de diseño utilizados.
- **[📝 Referencia de API y Datos](./docs/API_REFERENCE.md)**: Documentación sobre los modelos de datos (SQL), los esquemas Pydantic y los endpoints de la API.
- **[🤖 Guía de Desarrollo con IA](./docs/LLM_DEVELOPMENT.md)**: La hoja de ruta principal para el desarrollo iterativo, incluyendo los hitos del proyecto y la metodología de validación.

### Recursos Adicionales

- **[📓 Guía de Notebooks de Validación](./notebooks/README.md)**: Explica cómo usar los Jupyter Notebooks para probar y validar funcionalidades de forma aislada antes de su implementación final.
- **[💬 Guía de Prompts](./prompts/README.md)**: Describe la estructura de los prompts diseñados para guiar al asistente de IA en cada fase del desarrollo.
