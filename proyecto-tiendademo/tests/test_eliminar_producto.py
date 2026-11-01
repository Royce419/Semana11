"""Prueba funcional de eliminación de producto del carrito.

Este archivo valida que un producto agregado pueda ser eliminado y que ya no
aparezca en el carrito.
"""

import os
import unittest
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from utils.driver_factory import DriverFactory

BASE_URL = f"file:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'tienda_demo.html')).replace('\\', '/')}"

class TestEliminarProducto(unittest.TestCase):
    # Inicializa el driver y las páginas que se utilizarán.
    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.create_chrome()
        cls.catalog = CatalogPage(cls.driver)
        cls.cart = CartPage(cls.driver)

    # Cierra el navegador luego de ejecutar todas las pruebas.
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Agrega un producto y abre el carrito antes de cada prueba.
    def setUp(self):
        self.catalog.open(BASE_URL)
        self.catalog.add_product('Laptop Pro 15')
        self.catalog.open_cart()

    # Caso de prueba: eliminar un producto y verificar que desaparece.
    def test_eliminar_producto(self):
        self.cart.remove_item('Laptop Pro 15')
        self.assertFalse(self.cart.get_item_row('Laptop Pro 15'))

if __name__ == '__main__':
    unittest.main()
