import pytest

def test_CP_32(tienda):
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
    cat.agregar(); assert cat.contador() == 1 and "agregado" in cat.text("#toast")

def test_CP_33(tienda):
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
    preparar(); assert cart.cantidad() == 1 and cart.total() == 2499

def test_CP_34(tienda):
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
    preparar(); cart.cupon(); assert cart.visible("#fila-descuento") and cart.total() == 2249.10

def test_CP_35(tienda):
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
    comprar(); assert checkout.exito()

def test_CP_36(tienda):
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
    preparar(); cart.pagar(); checkout.completar(email="", direccion=""); checkout.confirmar(); assert checkout.visible("#error-email") and checkout.visible("#error-direccion")

def test_CP_37(tienda):
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
    comprar(); assert "Confirmado" in checkout.text("#detalle-orden") and checkout.text("#numero-orden").startswith("ORD-")

def test_CP_38(tienda):
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
    comprar(varios=True); assert checkout.exito() and "2,588.90" in checkout.text("#detalle-orden")

def test_CP_39(tienda):
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
    cat.abrir_carrito(); assert cart.visible("#carrito-vacio") and not cart.visible("#btn-ir-checkout")

def test_CP_40(tienda):
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
    preparar(varios=True); cart.cupon(); assert cart.total() == 2330.01; cart.pagar(); assert checkout.text("#total-checkout") == "S/ 2,330.01"

def test_CP_41(tienda):
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
    preparar(); cart.cupon(); cart.pagar(); checkout.completar(); checkout.confirmar(); assert checkout.exito() and "2,249.10" in checkout.text("#detalle-orden")

