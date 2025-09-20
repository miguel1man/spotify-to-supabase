# 📝 Scripts de Migración de Base de Datos

Este directorio contiene los scripts SQL necesarios para configurar el esquema de la base de datos en Supabase.

## 🚀 Cómo Ejecutar los Scripts

Para crear la estructura de tablas necesaria para la aplicación, debes ejecutar estos scripts en el **SQL Editor** de tu proyecto de Supabase.

Sigue estos pasos:

1.  **Navega al SQL Editor**:
    *   Abre tu proyecto en [app.supabase.com](https://app.supabase.com).
    *   En el menú de la izquierda, haz clic en el icono de la base de datos y selecciona **SQL Editor**.
    *   Haz clic en **+ New query**.

2.  **Copia y Pega el Código SQL**:
    *   Abre cada archivo `.sql` de este directorio **en el orden numérico de sus nombres**.
    *   Copia el contenido completo de un archivo.
    *   Pega el contenido en la ventana del editor de consultas de Supabase.

3.  **Ejecuta la Consulta**:
    *   Haz clic en el botón **RUN** (o usa el atajo `Cmd+Enter` / `Ctrl+Enter`).
    *   Deberías ver un mensaje de "Success. No rows returned".

4.  **Repite para todos los archivos**:
    *   Repite los pasos 2 y 3 para cada uno de los siguientes archivos, en este orden estricto:
        1.  `01_create_spotify_artists_table.sql`
        2.  `02_create_spotify_albums_table.sql`
        3.  `03_create_spotify_tracks_table.sql`
        4.  `04_create_spotify_track_artists_table.sql`
        5.  `05_create_spotify_album_artists_table.sql`
        6.  `06_create_track_details_view.sql`

Una vez que hayas ejecutado todos los scripts, tu base de datos estará lista para ser utilizada por la aplicación.
