# Jenkins en TiendaDemo

## Objetivo

Automatizar los 41 casos de Selenium y los 41 casos de Playwright, conservar sus resultados y permitir repetir la ejecucion desde Jenkins. Las pruebas utilizan el HTML local y navegadores sin ventana; no requieren iniciar el servidor de la tienda.

## Componentes

- Jenkins LTS 2.580.1: coordina las ejecuciones.
- Java 21: ejecuta Jenkins. Python ejecuta las pruebas.
- Python 3.10 o superior, dependencias de `requirements.txt`, Chrome y Chromium de Playwright.
- `scripts/ci.sh`: ejecuta ambas suites, genera XML JUnit y devuelve error si alguna suite falla.
- `scripts/start_jenkins.py` y `scripts/jenkins-init.groovy`: preparan el servidor y el trabajo local.
- `Jenkinsfile`: pipeline para un futuro repositorio Git con plugins Pipeline, Git y JUnit.

## Instalacion local en este Mac

Los binarios y la configuracion se guardan en `.jenkins-local/`, excluida de Git. No se instala un servicio del sistema. El servidor escucha solamente en `127.0.0.1:8081`, requiere autenticacion y no permite lectura anonima.

Para reproducir la descarga en un Mac Apple Silicon, desde la raiz del proyecto:

```bash
mkdir -p .jenkins-local/runtime
curl -fL https://get.jenkins.io/war-stable/2.580.1/jenkins.war -o .jenkins-local/runtime/jenkins.war
curl -fL https://api.adoptium.net/v3/binary/latest/21/ga/mac/aarch64/jre/hotspot/normal/eclipse -o .jenkins-local/runtime/java.tar.gz
tar -xzf .jenkins-local/runtime/java.tar.gz -C .jenkins-local/runtime
python3 scripts/start_jenkins.py
```

Antes de arrancar, verifica que no exista otra instancia en ese puerto. Para otros equipos utiliza una distribucion Java adecuada a su arquitectura.

El trabajo local reutiliza `.venv`, Chrome y el Chromium que ya usa el proyecto. Si faltan dependencias, sigue primero la instalacion del README.

## Acceso y ejecucion

1. Abre <http://127.0.0.1:8081>.
2. Inicia sesion con el usuario `admin`. La clave se encuentra en `.jenkins-local/admin-password`; puedes consultarla en tu terminal con `cat .jenkins-local/admin-password`. No incluyas la clave en la entrega.
3. Entra en `TiendaDemo-Pruebas` y pulsa **Build Now / Construir ahora**.
4. Abre la ejecucion y consulta **Console Output / Salida de consola**.
5. Consulta los archivos de **Artifacts / Artefactos**: XML, logs y capturas de ambas herramientas.

El trabajo local es de tipo Freestyle: ejecuta `scripts/ci.sh` y archiva los resultados con funciones del nucleo de Jenkins, sin plugins adicionales. Se ejecuta manualmente y utiliza el codigo de esta carpeta. No existe todavia integracion automatica con GitHub.

Cada build almacena sus evidencias en el workspace de Jenkins, en `evidencias/<numero-build>/`. Las ejecuciones anteriores del proyecto se conservan. Si falla Selenium, Playwright se ejecuta igualmente; Jenkins marca el trabajo como fallido si cualquiera devuelve un error.

En el trabajo local los XML se descargan como artefactos. Para mostrar un panel de resultados de pruebas en Jenkins, instala el plugin JUnit y agrega la accion posterior **Publish JUnit test result report**, con `evidencias/**/resultados.xml`.

## Pipeline cuando exista un repositorio Git

1. Sube el codigo y el `Jenkinsfile` a tu repositorio, excluyendo `.jenkins-local/`, entornos, caches y claves.
2. Instala los plugins **Pipeline**, **Git** y **JUnit** desde **Manage Jenkins > Plugins**.
3. Crea un trabajo de tipo **Pipeline**.
4. Selecciona **Pipeline script from SCM**, **Git**, la URL de tu repositorio y su rama real. Usa **Credentials** si el repositorio es privado.
5. Define **Script Path** como `Jenkinsfile`, guarda y ejecuta **Build Now**.

El agente debe ser macOS o Linux, tener Python y Chrome instalados, acceso a Internet para descargar dependencias y las bibliotecas del sistema necesarias para Chromium. En Linux puedes instalar esas bibliotecas previamente con `python -m playwright install-deps chromium`, con permisos de administrador. El pipeline usa Bash; no esta preparado para agentes Windows.

El `Jenkinsfile` crea `.venv-ci`, instala dependencias y Chromium, ejecuta las suites y publica XML y artefactos incluso ante fallos. Mantiene diez builds y limita la ejecucion a treinta minutos. Las evidencias de cada build tienen una carpeta propia. Los disparadores por cambios de Git requieren configurar adicionalmente un webhook o sondeo del repositorio.

## Evidencias para la entrega

Incluye esta guia, el `Jenkinsfile` y evidencia de una ejecucion real:

- Pantalla del trabajo y numero de build con su estado final.
- Salida de consola con los resumenes de ambas suites.
- Lista de artefactos con XML y capturas disponibles.
- Los XML y las capturas de los casos de esa misma ejecucion.

Una ejecucion completa sin fallos debe registrar 41 casos aprobados por herramienta. No atribuyas a Jenkins los resultados de ejecuciones anteriores hechas en terminal. El resultado observado de la configuracion local se registra al final de esta guia cuando termina el build.

## Detener y volver a iniciar

Para detener el proceso local desde la raiz:

```bash
kill "$(cat .jenkins-local/jenkins.pid)"
```

Para volver a iniciar:

```bash
python3 scripts/start_jenkins.py
```

La configuracion, el usuario y el historial persisten en `.jenkins-local/home`. Los logs del servidor estan en `.jenkins-local/jenkins.log`. El script de inicio no debe ejecutarse dos veces mientras el servidor siga activo.

## Problemas frecuentes

| Problema | Solucion |
| --- | --- |
| Puerto 8081 ocupado | Deten la instancia anterior antes de iniciar otra. |
| No se encuentra Java | Completa y extrae la descarga del runtime. |
| No se encuentra `.venv/bin/python` | Crea el entorno e instala `requirements.txt` como indica el README. |
| Selenium no inicia | Verifica Chrome y el acceso de Selenium Manager al driver. |
| Chromium no se encuentra | Instala Playwright Chromium con la ruta de cache indicada en el README. |
| Build fallido | Revisa la consola y los logs; identifica si fallo la preparacion, el navegador o una asercion. |
| No existe captura de un caso | Si el navegador no inicia, no puede generarse la captura. Revisa el XML y el log. |

## Referencias oficiales

- [Instalacion con WAR](https://www.jenkins.io/doc/book/installing/war-file/).
- [Compatibilidad con Java](https://www.jenkins.io/doc/book/platform-information/support-policy-java/).
- [Uso de Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/).

## Resultado verificado

La configuracion local se comprobo mediante el trabajo Freestyle `TiendaDemo-Pruebas`, build **#1**, con estado **SUCCESS**. Selenium registro **41 aprobados en 95.87 segundos** y Playwright **41 aprobados en 39.63 segundos**, sin fallos, errores ni casos omitidos.

La ejecucion se realizo el **9 de octubre de 2026, hora de Lima**. Se archivaron 86 archivos: 82 capturas de casos, 2 XML y 2 logs. La evidencia exportada esta en `evidencias/jenkins/build-1/`:

- `resumen.json`: estado y conteos por herramienta.
- `build.json`: metadatos del build obtenidos de la API de Jenkins.
- `consola.log`: salida real de Jenkins.
- `selenium-resultados.xml` y `playwright-resultados.xml`: resultados de la ejecucion.
- `artefactos.zip`: archivos publicados por Jenkins para este build.
- `01-trabajo.png`, `02-build.png`, `03-consola.png`, `04-artefactos.png`: pantallas de Jenkins despues de la ejecucion.

El archivo `documentacion_jenkins.zip` reune esta guia, el README, el Jenkinsfile, los scripts, `conftest.py` y las evidencias exportadas. No incluye el runtime, la configuracion privada del servidor ni la clave del administrador.

El pipeline del `Jenkinsfile` queda preparado para Git y no fue ejecutado en esta verificacion. La integracion automatica por cambios en un repositorio y el panel JUnit requieren los pasos adicionales indicados arriba.
