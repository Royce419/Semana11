"""Prueba funcional de agregar producto al carrito.

Este archivo valida que un usuario pueda seleccionar un producto desde el catálogo
y que el contador del carrito aumente correctamente.
"""

import os
import unittest
from pages.catalog_page import CatalogPage
from utils.driver_factory import DriverFactory

BASE_URL = f"file:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'tienda_demo.html')).replace('\\', '/')}"

class TestAgregarProducto(unittest.TestCase):
    # Configura el navegador y los objetos de página una sola vez.
    @classmethod
    def setUpClass(cls):
        cls.driver = DriverFactory.create_chrome()
        cls.catalog = CatalogPage(cls.driver)

    # Cierra el navegador cuando terminan todas las pruebas.
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    # Abre la página principal antes de cada prueba.
    def setUp(self):
        self.catalog.open(BASE_URL)

    # Caso de prueba: agregar un producto y validar el contador.
    def test_agregar_producto(self):
        self.catalog.add_product('Laptop Pro 15')
        self.assertEqual(self.catalog.get_cart_count(), 1)

if __name__ == '__main__':
    unittest.main()
