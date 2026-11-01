from utils.ui_base import BasePage
class CatalogoPage(BasePage):
    def agregar(self, producto=1):
        self.click(f"#btn-agregar-{producto}")
    def abrir_carrito(self):
        self.click("#btn-abrir-carrito")
    def contador(self):
        return int(self.text("#contador-carrito"))
