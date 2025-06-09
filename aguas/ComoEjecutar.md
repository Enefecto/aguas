# Documentación de como ejecutar el proyecto despues de haber copiado el repositorio.

Seguir el paso a paso si recién hiciste un git clone al repositorio para poder ejecutar correctamente el proyecto

## 1. Requisitos previos

- Tener instalado python y nodejs

## 2. Instalación previa a ejecución

Crear entorno virtual

- ```cmd
      python -m venv venv
  ```

Iniciar entorno virtual

- ```cmd
    .\venv\Scripts\Activate.ps1
  ```

Instalar dependencias

- ```cmd
    pip install -r requirements.txt
  ```

Entrar en el proyecto django

- ```cmd
    cd aguas
  ```

Instalar tailwind en el proyecto de django

- ```cmd
    python manage.py tailwind install
  ```

## 3. Ejecución en paralelo (2 Consolas)

Ejecutar el watcher que recompila tu CSS cada vez que detecta cambios en archivos

- ```cmd
    python manage.py tailwind start
  ```

Iniciar aplicación de Django que corre en http://127.0.0.1:8000/ y sirve el CSS compilado.

- ```cmd
    python manage.py runserver
  ```

## 4. Uso en html (Ocasional)

En caso de crear nuevas paginas de html en templates agregar lo siguiente:

Se agrega en la primera linea antes de `<html lang="es">`

- ```html
  {% load static tailwind_tags %}
  ```

Se agrega dentro de las etiquetas `<head>`

- ```html
  {% tailwind_css %}
  ```

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
