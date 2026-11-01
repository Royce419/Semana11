# TiendaDemo — Selenium y Playwright

Automatización con Python, Pytest y Page Object Model de los 41 casos de las capturas: CP-01 a CP-31 funcionales y CP-32 a CP-41 de aceptación (UAT). Cada herramienta tiene los casos distribuidos en cinco archivos, nunca en un único archivo.

## Estructura

```text
app/                         # Aplicación HTML, CSS y JS
selenium/pages/              # Catálogo, carrito y checkout (POM)
selenium/tests/              # CP-01–05, 06–13, 14–19, 20–31, 32–41
playwright/pages/            # Catálogo, carrito y checkout (POM)
playwright/tests/            # Los mismos cinco grupos
utils/ui_base.py             # Base de los Page Objects
utils/ui_adapters.py         # Operaciones propias de cada herramienta
conftest.py                  # Navegador aislado por caso y capturas automáticas
pytest.ini                  # Descubrimiento de las dos suites
evidencias/selenium/        # Capturas agrupadas por ejecución
evidencias/playwright/
pages/, tests/, features/    # Pruebas originales de unittest y Behave
```

## 1. Instalar desde la terminal (macOS / Linux)

Necesitas Python 3.10 o superior y Google Chrome para Selenium. Abre la terminal en la carpeta del proyecto:

```bash
cd "/Users/rk/Desktop/PROYECTOS DE SOTFWARE/proyecto-tiendademo"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
PLAYWRIGHT_BROWSERS_PATH="$PWD/.cache/ms-playwright" python -m playwright install chromium
```

En Windows establece también `$env:PLAYWRIGHT_BROWSERS_PATH = "$PWD/.cache/ms-playwright"` antes de `python -m playwright install chromium`. En Windows, entra en la carpeta del proyecto y utiliza `py -m venv .venv` y `.venv\Scripts\Activate.ps1` para crear y activar el entorno; los demás comandos con `python` son iguales.

Selenium Manager obtiene el driver de Chrome automáticamente. La primera instalación y la descarga de navegadores requieren Internet. Referencias: [Selenium Manager](https://www.selenium.dev/documentation/selenium_manager/) y [Playwright para Python](https://playwright.dev/python/docs/library).

## 2. Abrir la aplicación

En una primera terminal:

```bash
source .venv/bin/activate
python -m http.server 8000 --bind 127.0.0.1 --directory app
```

Abre <http://127.0.0.1:8000/tienda_demo.html>. Si el puerto ya está ocupado por el servidor de TiendaDemo, utiliza el servidor existente o detén el anterior con Ctrl+C.

Las pruebas abren el HTML local de forma predeterminada y no requieren el servidor. Para probar contra el servidor, en la terminal de las pruebas establece:

```bash
export BASE_URL="http://127.0.0.1:8000/tienda_demo.html"
```

## 3. Ejecutar pruebas y guardar resultados

En otra terminal, desde la misma carpeta:

```bash
source .venv/bin/activate
mkdir -pevidencias/seleniumevidencias/playwright
python -m pytest selenium/tests -v --junitxml=evidencias/selenium/resultados.xml
python -m pytest playwright/tests -v --junitxml=evidencias/playwright/resultados.xml
```

Ejecutar ambas herramientas:

```bash
python -m pytest -v
```

Mostrar el navegador mientras se ejecuta:

```bash
python -m pytest selenium/tests -v --headed
python -m pytest playwright/tests -v --headed
```

Ejecutar un grupo o un caso:

```bash
python -m pytest selenium/tests/test_tc01_tc05.py -v
python -m pytest playwright/tests/test_tc20_tc31.py -v
python -m pytest selenium/tests -k test_CP_01 -v
python -m pytest playwright/tests -k test_CP_41 -v
```

Cada caso usa un navegador o contexto nuevo. Se guarda automáticamente una captura PNG de su estado final, también cuando falla, se omite o queda como fallo esperado. Si el navegador no llega a iniciar, no puede generarse una captura.

## 4. Capturas y entrega de evidencias

1. Ejecuta las dos suites con los comandos anteriores.
2. Revisa las carpetas `evidencias/selenium/<fecha-hora>/` y `evidencias/playwright/<fecha-hora>/`. Cada una contiene archivos como `test_CP_01.png` y `test_CP_41.png`; conserva los de la ejecución que entregarás.
3. Toma además una captura de la terminal con el comando y el resumen final de cada herramienta (en macOS, Cmd+Shift+4). Guárdala como `resumen_terminal.png` dentro de la carpeta de esa ejecución.
4. Adjunta los PNG al registro de casos según su identificador CP y la herramienta. Registra el resultado real: aprobado, fallido, omitido o fallo esperado; una captura por sí sola no acredita aprobación.
5. Incluye los XML de resultados y, si tu tarea lo pide, el registro de casos y la matriz de trazabilidad. La matriz está completada en `matriz_trazabilidad.xlsx` con los 41 casos.
6. Comprime las evidencias desde la raíz:

```bash
zip -r evidencias_tiendademo.zip evidencias
```

7. En tu aula virtual o plataforma de entrega, selecciona **Adjuntar archivo / Subir archivo**, elige el ZIP y confirma la entrega. No se realiza ninguna subida automática; la plataforma y sus requisitos adicionales no aparecen en las capturas proporcionadas.

Los PNG y XML generados están excluidos de Git para evitar subirlos por accidente. Si tu entrega exige incluirlos en un repositorio, selecciona expresamente la carpeta de la ejecución:

```bash
git add -fevidencias/selenium/FECHA-DE-LA-EJECUCION/
git add -fevidencias/playwright/FECHA-DE-LA-EJECUCION/
```

Sustituye `FECHA-DE-LA-EJECUCION` por el nombre real. Revisa lo preparado antes de hacer commit.

## 5. Requisitos corregidos

- **CP-08:** puedes escribir cantidad 0; al salir del campo, se elimina el producto.
- **CP-09:** puedes ingresar una cantidad negativa; se rechaza con un mensaje y se restablece la cantidad anterior, manteniendo contador y total. También se rechazan cantidades vacías, decimales y superiores al stock.
- **CP-17:** reaplicar el mismo cupón muestra un aviso y conserva el descuento sin duplicarlo.
- **CP-23:** el checkout incluye el campo Apellido y valida que sea obligatorio. Nombre y apellido aparecen juntos en la confirmación.
- **CP-20 / CP-39:** el carrito vacío muestra su mensaje y no ofrece el botón de pago.

Las suites ya no omiten CP-09 ni marcan CP-17 o CP-23 como fallos esperados. Los 41 casos de cada herramienta deben aprobarse; el resultado real se obtiene al ejecutar las pruebas.

## Jenkins

La configuracion y documentacion de Jenkins estan en [docs/JENKINS.md](docs/JENKINS.md). Incluye un trabajo local para ejecutar Selenium y Playwright, guardar las evidencias de cada build y un `Jenkinsfile` para integrar el proyecto con Git posteriormente.

Jenkins local: <http://127.0.0.1:8081>. El trabajo `TiendaDemo-Pruebas`, build #1, termino con SUCCESS: 41 aprobados en Selenium y 41 en Playwright. La documentacion y las evidencias de Jenkins se entregan en `documentacion_jenkins.zip`.

## Pruebas originales

Se conservan las pruebas previas; no forman parte del descubrimiento predeterminado de las nuevas suites:

```bash
python -m unittest discover -s tests
behave features
```

## Solución de problemas

- `No module named ...`: activa `.venv` e instala `requirements.txt` con ese mismo Python.
- Playwright indica que falta el ejecutable: ejecuta `PLAYWRIGHT_BROWSERS_PATH="$PWD/.cache/ms-playwright" python -m playwright install chromium`.
- Selenium no abre Chrome: verifica su instalación y la conexión necesaria para descargar el driver.
- `Connection refused`: inicia el servidor si estableciste `BASE_URL`, o usa `unset BASE_URL` para volver al HTML local.
- No aparecen evidencias: revisa primero si el navegador pudo iniciar; las capturas se guardan al terminar cada caso.


## Verificación después de corregir los requisitos

El 9 de octubre de 2026 se ejecutaron las suites completas: **41 aprobados en Selenium y 41 aprobados en Playwright**, sin casos omitidos ni fallos esperados. También aprobaron las 7 pruebas originales de unittest y los 4 escenarios de Behave.

Evidencias finales:

- Selenium: `evidencias/selenium/20261009-223839-549461/`.
- Playwright: `evidencias/playwright/20261009-223607-029894/`.
- `evidencias_tiendademo.zip`: actualizado con las 82 capturas finales y los dos XML de resultados. Las ejecuciones anteriores se conservan para revisión y no se incluyen en ese ZIP.

Recarga la página de la tienda para ver el campo Apellido y la cantidad editable. Para entregar, adjunta el ZIP y la captura del resumen de tu terminal en la plataforma indicada por tu curso.

## Matriz de trazabilidad

`matriz_trazabilidad.xlsx` contiene TC-01 a TC-41, equivalentes a CP-01 a CP-41. Mantiene las columnas exigidas: ID, Tipo, Selenium, Playwright, Assertion y Evidencia. Incluye 31 casos funcionales y 10 UAT, los resultados de los XML, las funciones de prueba y las rutas de las 82 capturas verificadas. El ZIP de entrega se actualizó para incluir la matriz y las evidencias citadas en ella. Los resultados de la matriz son una instantánea; después de nuevas ejecuciones deben actualizarse junto con las rutas de evidencia.
