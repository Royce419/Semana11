"""Pasos de Behave para validar el flujo del carrito de compras."""

from behave import given, when, then
from selenium.webdriver.common.by import By
from utils.driver_factory import DriverFactory
import os

# Genera la URL local del archivo HTML de la aplicación.
BASE_URL = f"file:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'tienda_demo.html')).replace('\\', '/')}"

@given('estoy en el catálogo de TiendaDemo')
def step_impl(context):
    # Inicia el navegador y abre la página del catálogo.
    context.driver = DriverFactory.create_chrome()
    context.driver.get(BASE_URL)

@when('agrego "{producto}" al carrito')
def step_impl(context, producto):
    # Busca el producto en el catálogo y hace clic en el botón Agregar.
    buttons = context.driver.find_elements(By.CSS_SELECTOR, '.tarjeta-producto')
    for card in buttons:
        if producto in card.text:
            card.find_element(By.CSS_SELECTOR, '.btn-agregar').click()
            return
    raise AssertionError(f'Producto {producto} no encontrado')

@then('veo el producto "{producto}" en el carrito')
def step_impl(context, producto):
    # Abre el carrito y valida que el producto aparezca en la página.
    context.driver.find_element(By.ID, 'btn-abrir-carrito').click()
    assert producto in context.driver.page_source

@when('abro el carrito')
def step_impl(context):
    # Hace clic en el botón para mostrar la vista del carrito.
    context.driver.find_element(By.ID, 'btn-abrir-carrito').click()

@when('aplico el cupón "{cupon}"')
def step_impl(context, cupon):
    # Ingresa y aplica un cupón en la vista del carrito.
    context.driver.find_element(By.ID, 'input-cupon').send_keys(cupon)
    context.driver.find_element(By.ID, 'btn-aplicar-cupon').click()

@then('veo el mensaje de cupón aplicado')
def step_impl(context):
    # Verifica que el mensaje de cupón esté visible.
    assert 'Cupón' in context.driver.find_element(By.ID, 'msg-cupon').text

@given('tengo un producto en el carrito')
def step_impl(context):
    # Reutiliza otros pasos para preparar el estado del carrito.
    context.execute_steps('''
        Given estoy en el catálogo de TiendaDemo
        When agrego "Laptop Pro 15" al carrito
        When abro el carrito
    ''')
