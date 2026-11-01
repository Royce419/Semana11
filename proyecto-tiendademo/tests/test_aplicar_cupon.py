"""Prueba funcional de aplicación de cupones en el carrito.

Incluye la validación de un cupón válido y de un cupón inválido, para asegurar
que el sistema maneje ambos casos.
"""

import os
import unittest
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from utils.driver_factory import DriverFactory

BASE_URL = f"file:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'tienda_demo.html')).replace('\\', '/')}"

class TestAplicarCupon(unittest.TestCase):
    # Inicializa el navegador y las páginas de test.
    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.create_chrome()
        cls.catalog = CatalogPage(cls.driver)
        cls.cart = CartPage(cls.driver)

    # Cierra el navegador una vez finalizadas las pruebas.
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Prepara el carrito con un producto antes de cada test.
    def setUp(self):
        self.catalog.open(BASE_URL)
        self.catalog.add_product('Teclado Mecánico')
        self.catalog.open_cart()

    # Verifica que un cupón válido sea aceptado.
    def test_aplicar_cupon_valido(self):
        self.cart.apply_coupon('DESCUENTO10')
        self.assertIn('DESCUENTO10', self.cart.get_coupon_message())

    # Verifica que un cupón inválido muestre un mensaje de error.
    def test_aplicar_cupon_invalido(self):
        self.cart.apply_coupon('INVALIDO')
        self.assertIn('Cupón no válido', self.cart.get_coupon_message())

if __name__ == '__main__':
    unittest.main()
