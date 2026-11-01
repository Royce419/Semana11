from utils.ui_base import BasePage
class CartPage(BasePage):
    def cantidad(self, producto=1):
        return int(self.ui.value(f"#cantidad-{producto}"))
    def establecer_cantidad(self, cantidad, producto=1):
        self.ui.fill(f"#cantidad-{producto}", str(cantidad))
        self.click("#vista-carrito h2")
    def aumentar(self, producto=1):
        self.click(f"#btn-mas-{producto}")
    def reducir(self, producto=1):
        self.click(f"#btn-menos-{producto}")
    def eliminar(self, producto=1):
        self.click(f"#btn-eliminar-{producto}")
    def cupon(self, codigo="DESCUENTO10"):
        self.ui.fill("#input-cupon", codigo)
        self.click("#btn-aplicar-cupon")
    def pagar(self):
        self.click("#btn-ir-checkout")
    def total(self):
        return float(self.text("#valor-total").replace("S/", "").replace(",", "").strip())
