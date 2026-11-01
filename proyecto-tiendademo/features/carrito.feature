Feature: Carrito de compras
  Como usuario quiero agregar, modificar y eliminar productos del carrito
  Para completar una compra con éxito

  Scenario: Agregar un producto al carrito
    Given estoy en el catálogo de TiendaDemo
    When agrego "Laptop Pro 15" al carrito
    Then veo el producto "Laptop Pro 15" en el carrito

  Scenario: Aplicar un cupón válido
    Given tengo un producto en el carrito
    When abro el carrito
    And aplico el cupón "DESCUENTO10"
    Then veo el mensaje de cupón aplicado
