import pytest

def test_CP_01(tienda):
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
    cat.agregar(); cat.abrir_carrito(); assert cart.visible("#item-1") and cat.contador() == 1

def test_CP_02(tienda):
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
    cat.agregar(); cat.agregar(2); cat.abrir_carrito(); assert cart.visible("#item-1") and cart.visible("#item-2")

def test_CP_03(tienda):
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
    cat.agregar(); cat.agregar(); cat.abrir_carrito(); assert cart.cantidad() == 2 and cat.contador() == 2

def test_CP_04(tienda):
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
    cat.agregar(); assert cat.contador() == 1

def test_CP_05(tienda):
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
    cat.agregar(); cat.abrir_carrito(); assert "Laptop Pro 15" in cart.text("#item-1")

