# Documentación de como ejecutar el proyecto despues de haber copiado el repositorio.

## 1. Requisitos previos

## 2. Ejecución en paralelo (2 Consolas)

- ```cmd
    python manage.py tailwind start
  ```

  Esto mantiene un watcher que recompila tu CSS cada vez que detecta cambios en archivos

- ```cmd
    python manage.py runserver
  ```
  Tu aplicación Django corre en http://127.0.0.1:8000/ y sirve el CSS compilado.

## 3. Uso en html (Ocasional)

- ```html
  {% load static tailwind_tags %}
  ```

  Se agrega en la primera linea antes de `<html lang="es">`

- ```html
  {% tailwind_css %}
  ```

  Se agrega dentro de las etiquetas `<head>`

Ejemplo:

- ```html
  {% load static tailwind_tags %}
  <!DOCTYPE html>
  <html lang="es">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Ejemplo</title>
      {% tailwind_css %}
    </head>
    <body>
      <h1 class="text-4xl">Hola Documentación</h1>
    </body>
  </html>
  ```
