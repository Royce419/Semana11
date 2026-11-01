"""Prueba funcional de modificación de cantidad en el carrito.

Este archivo verifica que sea posible aumentar la cantidad de un producto
desde la vista del carrito y que el sistema refleje la cantidad correcta.
"""

import os
import unittest
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from utils.driver_factory import DriverFactory

BASE_URL = f"file:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'tienda_demo.html')).replace('\\', '/')}"

class TestModificarCantidad(unittest.TestCase):
    # Configura el driver y las páginas necesarias para el test.
    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.create_chrome()
        cls.catalog = CatalogPage(cls.driver)
        cls.cart = CartPage(cls.driver)

    # Cierra el navegador al final de la suite.
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Prepara el estado con un producto agregado al carrito.
    def setUp(self):
        self.catalog.open(BASE_URL)
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()

    # Caso de prueba: incrementar la cantidad de un producto.
    def test_modificar_cantidad(self):
        self.cart.increase_quantity('Laptop Pro 15')
        self.assertEqual(self.cart.get_quantity('Laptop Pro 15'), 2)

if __name__ == '__main__':
    unittest.main()
