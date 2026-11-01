import pytest

def test_CP_06(tienda):
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
    preparar(); cart.aumentar(); assert cart.cantidad() == 2 and cart.total() == 4998

def test_CP_07(tienda):
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
    cat.agregar(); preparar(); cart.reducir(); assert cart.cantidad() == 1 and cart.total() == 2499

def test_CP_08(tienda):
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
    preparar(); cart.establecer_cantidad(0); assert cart.visible("#carrito-vacio") and cat.contador() == 0

def test_CP_09(tienda):
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
    preparar(); cart.establecer_cantidad(-1); assert cart.cantidad() == 1 and cart.total() == 2499 and "cantidad entera" in cat.text("#toast")

def test_CP_10(tienda):
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
    preparar(varios=True); cart.eliminar(); assert not cart.visible("#item-1")

def test_CP_11(tienda):
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
    preparar(); cart.eliminar(); assert cart.visible("#carrito-vacio")

def test_CP_12(tienda):
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
    preparar(varios=True); cart.eliminar(); assert not cart.visible("#item-1") and cart.visible("#item-2")

def test_CP_13(tienda):
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
    preparar(varios=True); cart.eliminar(); assert cart.text("#valor-subtotal") == "S/ 89.90" and cart.total() == 89.90

