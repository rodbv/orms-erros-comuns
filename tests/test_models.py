import re
from decimal import Decimal

import pytest
from model_bakery import baker


@pytest.mark.django_db
def test_pedido_num_pedido_gerado_com_formato_valido_e_unico():
    cliente = baker.make("api.Cliente")

    pedido_1 = baker.make(
        "api.Pedido",
        cliente=cliente,
        valor_total=Decimal("100.00"),
        numero_pedido="PED-0001",
    )
    pedido_2 = baker.make(
        "api.Pedido",
        cliente=cliente,
        valor_total=Decimal("200.00"),
        numero_pedido="PED-0002",
    )

    padrao = r"^[A-Z]{3}[0-9]{3}[A-Z]$"

    assert re.fullmatch(padrao, pedido_1.num_pedido)
    assert re.fullmatch(padrao, pedido_2.num_pedido)
    assert pedido_1.num_pedido != pedido_2.num_pedido


@pytest.mark.django_db
def test_pedido_num_pedido_nao_muda_em_update():
    pedido = baker.make(
        "api.Pedido",
        valor_total=Decimal("150.00"),
        numero_pedido="PED-0100",
    )
    num_pedido_original = pedido.num_pedido

    pedido.valor_total = Decimal("175.00")
    pedido.save()
    pedido.refresh_from_db()

    assert pedido.num_pedido == num_pedido_original
