import pytest

def test_CP_20(tienda):
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
    cat.abrir_carrito(); assert cart.visible("#carrito-vacio") and not cart.visible("#btn-ir-checkout") and not checkout.visible("#vista-checkout")

def test_CP_21(tienda):
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
    preparar(); cart.pagar(); checkout.confirmar(); assert all(checkout.visible("#error-" + campo) for campo in ["nombre", "apellido", "email", "direccion", "ciudad", "telefono"])

def test_CP_22(tienda):
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
    validar("nombre", "")

def test_CP_23(tienda):
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
    validar("apellido", "")

def test_CP_24(tienda):
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
    validar("email", "")

def test_CP_25(tienda):
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
    validar("email", "correo-sin-arroba")

def test_CP_26(tienda):
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
    validar("telefono", "")

def test_CP_27(tienda):
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
    validar("direccion", "")

def test_CP_28(tienda):
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

def test_CP_29(tienda):
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

def test_CP_30(tienda):
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
    comprar(); assert checkout.visible("#confirmacion-card") and checkout.text("#numero-orden").startswith("ORD-")

def test_CP_31(tienda):
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
    comprar(); checkout.seguir(); assert cat.visible("#vista-catalogo") and cat.contador() == 0

