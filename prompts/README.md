# 💬 Guía de Prompts para el Desarrollo

Este directorio contiene una serie de prompts estructurados en formato Markdown, diseñados para guiar a un asistente de IA en la construcción del proyecto, fase por fase.

## Propósito

El objetivo de estos prompts es dividir el complejo proceso de desarrollo de software en tareas más pequeñas, manejables y específicas. Cada archivo corresponde a un hito de desarrollo y contiene las instrucciones precisas que el LLM debe seguir.

Esto asegura que el desarrollo sea:
- **Consistente**: Sigue la arquitectura y los patrones predefinidos.
- **Incremental**: Construye la aplicación paso a paso.
- **Verificable**: Cada paso puede ser probado y validado.

## Estructura de los Prompts

Los prompts están organizados en directorios numerados que corresponden a las fases de desarrollo:

- **`01-setup/`**: Tareas relacionadas con la configuración inicial del proyecto, dependencias y estructura de directorios.
- **`02-authentication/`**: Instrucciones para implementar los flujos de autenticación con Spotify y la conexión con Supabase.
- **`03-core-features/`**: Prompts para desarrollar la lógica de negocio principal, como los clientes de API, los repositorios y los servicios de sincronización.
- **`04-api-endpoints/`**: Guías para crear los endpoints de la API REST con FastAPI, incluyendo la configuración de la documentación de Swagger.
- **`05-testing/`**: Tareas para escribir tests unitarios y de integración.

## Cómo Usar

El flujo de trabajo ideal es:
1.  El desarrollador (o un LLM de nivel superior) selecciona el prompt correspondiente al siguiente hito de desarrollo.
2.  El contenido del archivo `.md` se proporciona como la instrucción principal al LLM que tiene acceso a la CLI.
3.  El LLM ejecuta las instrucciones, que a menudo incluyen:
    - Leer archivos existentes para obtener contexto.
    - Ejecutar un notebook de validación.
    - Escribir o modificar el código fuente.
    - Ejecutar pruebas para verificar los cambios.
