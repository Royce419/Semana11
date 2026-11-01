# Hook de Behave que se ejecuta después de cada escenario.
# Se asegura de cerrar el navegador y liberar recursos.
def after_scenario(context, scenario):
    if hasattr(context, 'driver') and context.driver:
        context.driver.quit()
        context.driver = None
