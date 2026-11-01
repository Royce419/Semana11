import pytest

def test_CP_14(tienda):
    cat, cart, checkout = tienda
    def preparar(varios=False):
        cat.agregar()
        if varios:
            cat.agregar(2)
        cat.abrir_carrito()
    def comprar(varios=False):
        preparar(varios)
        cart.pagar()
        checkout.completar()
        checkout.confirmar()
    def validar(campo, valor):
        preparar()
        cart.pagar()
        checkout.completar(**{campo: valor})
        checkout.confirmar()
        assert checkout.visible("#error-" + campo)
        assert not checkout.exito()
    preparar(); cart.cupon(); assert "aplicado" in cart.text("#msg-cupon")

def test_CP_15(tienda):
    cat, cart, checkout = tienda
    def preparar(varios=False):
        cat.agregar()
        if varios:
            cat.agregar(2)
        cat.abrir_carrito()
    def comprar(varios=False):
        preparar(varios)
        cart.pagar()
        checkout.completar()
        checkout.confirmar()
    def validar(campo, valor):
        preparar()
        cart.pagar()
        checkout.completar(**{campo: valor})
        checkout.confirmar()
        assert checkout.visible("#error-" + campo)
        assert not checkout.exito()
    preparar(); cart.cupon("INVALIDO"); assert "no válido" in cart.text("#msg-cupon") and cart.total() == 2499

def test_CP_16(tienda):
    cat, cart, checkout = tienda
    def preparar(varios=False):
        cat.agregar()
        if varios:
            cat.agregar(2)
        cat.abrir_carrito()
    def comprar(varios=False):
        preparar(varios)
        cart.pagar()
        checkout.completar()
        checkout.confirmar()
    def validar(campo, valor):
        preparar()
        cart.pagar()
        checkout.completar(**{campo: valor})
        checkout.confirmar()
        assert checkout.visible("#error-" + campo)
        assert not checkout.exito()
    preparar(); cart.cupon(""); assert "Ingresa" in cart.text("#msg-cupon") and cart.total() == 2499

def test_CP_17(tienda):
    cat, cart, checkout = tienda
    def preparar(varios=False):
        cat.agregar()
        if varios:
            cat.agregar(2)
        cat.abrir_carrito()
    def comprar(varios=False):
        preparar(varios)
        cart.pagar()
        checkout.completar()
        checkout.confirmar()
    def validar(campo, valor):
        preparar()
        cart.pagar()
        checkout.completar(**{campo: valor})
        checkout.confirmar()
        assert checkout.visible("#error-" + campo)
        assert not checkout.exito()
    preparar(); cart.cupon(); total = cart.total(); cart.cupon(); assert "ya aplicado" in cart.text("#msg-cupon").lower() and cart.total() == total

def test_CP_18(tienda):
    cat, cart, checkout = tienda
    def preparar(varios=False):
        cat.agregar()
        if varios:
            cat.agregar(2)
        cat.abrir_carrito()
    def comprar(varios=False):
        preparar(varios)
        cart.pagar()
        checkout.completar()
        checkout.confirmar()
    def validar(campo, valor):
        preparar()
        cart.pagar()
        checkout.completar(**{campo: valor})
        checkout.confirmar()
        assert checkout.visible("#error-" + campo)
        assert not checkout.exito()
    preparar(); cart.cupon(); assert cart.total() == 2249.10

def test_CP_19(tienda):
    cat, cart, checkout = tienda
    def preparar(varios=False):
        cat.agregar()
        if varios:
            cat.agregar(2)
        cat.abrir_carrito()
    def comprar(varios=False):
        preparar(varios)
        cart.pagar()
        checkout.completar()
        checkout.confirmar()
    def validar(campo, valor):
        preparar()
        cart.pagar()
        checkout.completar(**{campo: valor})
        checkout.confirmar()
        assert checkout.visible("#error-" + campo)
        assert not checkout.exito()
    preparar(); assert cart.total() == 2499 and not cart.visible("#fila-descuento")

