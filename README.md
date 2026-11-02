# Entrega Semana 11

Repositorio de integración de los trabajos de aseguramiento de calidad de las semanas 8 y 9.

## Proyectos incluidos

- `proyecto-tiendademo/`: trabajo de Semana 8, con sus pruebas y documentación.
- `aula-nova-semana9/`: aplicación y pruebas de Semana 9 extraídas de `SEMANA9-main.zip`.

Los proyectos permanecen en carpetas separadas porque son aplicaciones distintas. Este repositorio es la base para completar la integración CI solicitada en Semana 11.

## Pipelines integrados

- GitHub Actions: `.github/workflows/semana8.yml` y `.github/workflows/semana9.yml`. Ambos se ejecutan en `push`, `pull_request` y manualmente desde Actions.
- Jenkins: `Jenkinsfile` en la raíz. Configura el job como **Pipeline script from SCM**, apunta a la rama `main` y usa `Jenkinsfile` como Script Path. El pipeline consulta cambios cada cinco minutos con Poll SCM.
- Docker Compose Semana 8: `docker-compose.semana8.yml`; la tienda queda en `http://127.0.0.1:8081/tienda_demo.html`.
- Docker Compose Semana 9: `docker-compose.semana9.yml`; Aula Nova queda en `http://127.0.0.1:3001`.

El agente Jenkins necesita Docker con Compose, Node.js 24, Python 3, Chrome/Chromium, k6 y acceso a Internet para instalar dependencias. Para usar GitHub Actions, los cambios deben estar publicados en el repositorio.

## TestLink pendiente de configuración

La tarea solicita registrar resultados en TestLink. Para conectar la instancia se necesitan el URL de la API XML-RPC, el proyecto y plan de pruebas, el build de TestLink y la correspondencia entre los identificadores locales (CP/CR/CE) y los casos de TestLink. Guarda la clave API como secreto en GitHub Actions y como credencial en Jenkins; no la escribas en este README ni en el Jenkinsfile.
