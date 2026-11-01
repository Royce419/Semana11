"""Pasos de Behave para validar el flujo de checkout y pago."""

from behave import given, when, then
from selenium.webdriver.common.by import By
from utils.driver_factory import DriverFactory
import os

# Constructor de URL local para abrir la aplicación en el navegador.
BASE_URL = f"file:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'tienda_demo.html')).replace('\\', '/')}"

@given('estoy en la página de checkout con un artículo en el carrito')
def step_impl(context):
    # Inicia el navegador, agrega un artículo y navega al checkout.
    context.driver = DriverFactory.create_chrome()
    context.driver.get(BASE_URL)
    context.driver.find_element(By.CSS_SELECTOR, '.tarjeta-producto .btn-agregar').click()
    context.driver.find_element(By.ID, 'btn-abrir-carrito').click()
    context.driver.find_element(By.ID, 'btn-ir-checkout').click()

@when('intento confirmar el pago sin completar los datos')
def step_impl(context):
    # Intenta enviar el formulario con campos obligatorios vacíos.
    context.driver.find_element(By.ID, 'btn-confirmar-pago').click()

@then('veo mensajes de error para los campos obligatorios')
def step_impl(context):
    # Verifica que aparezcan las validaciones de formulario.
    assert 'El nombre es obligatorio' in context.driver.page_source

@when('completo todos los datos y confirmo el pago')
def step_impl(context):
    # Llena los campos requeridos y confirma el pago.
    context.driver.find_element(By.ID, 'campo-nombre').send_keys('María')
    context.driver.find_element(By.ID, 'campo-apellido').send_keys('López')
    context.driver.find_element(By.ID, 'campo-email').send_keys('maria@correo.com')
    context.driver.find_element(By.ID, 'campo-direccion').send_keys('Jr. 9 de Octubre 456')
    context.driver.find_element(By.ID, 'campo-ciudad').send_keys('Lima')
    context.driver.find_element(By.ID, 'campo-telefono').send_keys('987654321')
    context.driver.find_element(By.ID, 'btn-confirmar-pago').click()

@then('veo la pantalla de confirmación')
def step_impl(context):
    # Comprueba que el mensaje de éxito se muestre después del pago.
    assert '¡Compra realizada con éxito!' in context.driver.page_source
