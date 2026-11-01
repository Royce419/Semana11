from utils.ui_base import BasePage
class CheckoutPage(BasePage):
    def completar(self, **cambios):
        datos = dict(nombre="Ana", apellido="Pérez", email="ana@example.com", direccion="Av. Principal 123", ciudad="Lima", telefono="987654321")
        datos.update(cambios)
        for campo, valor in datos.items():
            self.ui.fill(f"#campo-{campo}", valor)
    def confirmar(self):
        self.click("#btn-confirmar-pago")
    def exito(self):
        return self.visible("#msg-confirmacion") and "éxito" in self.text("#msg-confirmacion")
    def seguir(self):
        self.click("#btn-seguir-comprando")
