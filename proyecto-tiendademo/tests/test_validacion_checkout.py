"""Prueba funcional de validación del checkout.

Incluye casos de error cuando los datos son incompletos y un flujo exitoso
cuando se completa toda la información correctamente.
"""

import os
import unittest
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.driver_factory import DriverFactory

BASE_URL = f"file:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'tienda_demo.html')).replace('\\', '/')}"

class TestValidacionCheckout(unittest.TestCase):
    # Configura el navegador y los Page Objects una sola vez.
    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.create_chrome()
        cls.catalog = CatalogPage(cls.driver)
        cls.cart = CartPage(cls.driver)
        cls.checkout = CheckoutPage(cls.driver)

    # Finaliza la sesión del navegador.
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Deja el sistema en la vista de checkout con un producto agregado.
    def setUp(self):
        self.catalog.open(BASE_URL)
        self.catalog.add_product('Disco SSD 1TB')
        self.catalog.open_cart()
        self.cart.proceed_to_checkout()

    # Verifica la validación de campos obligatorios cuando no se completa el formulario.
    def test_checkout_form_validation(self):
        self.checkout.confirm_payment()
        errors = self.checkout.get_error_messages()
        self.assertTrue(any('obligatorio' in msg.lower() for msg in errors))

    # Verifica el flujo de checkout exitoso con datos válidos.
    def test_checkout_confirmacion_con_datos_validos(self):
        self.checkout.fill_shipping_info('María', 'maria@correo.com', 'Jr. 9 de Octubre 456', 'Lima', '987654321', surname='López')
        self.checkout.select_payment_method('yape')
        self.checkout.confirm_payment()
        self.assertIn('¡Compra realizada con éxito!', self.checkout.driver.page_source)

if __name__ == '__main__':
    unittest.main()
