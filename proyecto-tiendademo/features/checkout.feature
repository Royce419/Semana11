Feature: Checkout
  Como usuario quiero completar el pago
  Para recibir la confirmación del pedido

  Scenario: Validar campos obligatorios en checkout
    Given estoy en la página de checkout con un artículo en el carrito
    When intento confirmar el pago sin completar los datos
    Then veo mensajes de error para los campos obligatorios

  Scenario: Confirmar compra con datos válidos
    Given estoy en la página de checkout con un artículo en el carrito
    When completo todos los datos y confirmo el pago
    Then veo la pantalla de confirmación
