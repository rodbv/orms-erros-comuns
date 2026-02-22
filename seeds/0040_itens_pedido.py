from __future__ import annotations

import random
from decimal import Decimal

from django.db import transaction
from django.db.models import DecimalField, F, Sum

from api.models import ItemPedido, Pedido, Produto
from seeds.utils import apply_random_timestamps

NUM_ITENS = 2000

OBSERVACOES = [
    "",
    "Embalagem para presente",
    "Cliente pediu entrega rapida",
    "Nao substitui item em falta",
    "Conferir voltagem",
]


@transaction.atomic
def run(num_itens: int = NUM_ITENS) -> int:
    rng = random.Random(20260221)
    pedidos = list(Pedido.objects.select_related("cliente"))
    produtos = list(Produto.objects.all())

    if not pedidos or not produtos:
        raise ValueError("Seed de itens requer pedidos e produtos cadastrados")

    pedidos_processados = pedidos[:num_itens] if num_itens else pedidos
    itens = []
    contador_itens = {pedido.id: 0 for pedido in pedidos_processados}

    for pedido in pedidos_processados:
        quantidade_itens = rng.randint(1, 4)
        for _ in range(quantidade_itens):
            produto = rng.choice(produtos)
            quantidade = rng.randint(1, 3)
            contador_itens[pedido.id] += 1
            numero_item = contador_itens[pedido.id]

            valor_total = produto.valor_unitario * quantidade
            itens.append(
                ItemPedido(
                    pedido=pedido,
                    produto=produto,
                    quantidade=quantidade,
                    valor_unitario=produto.valor_unitario,
                    valor_total=valor_total,
                    observacoes=rng.choice(OBSERVACOES),
                    numero_item=numero_item,
                    cancelado=rng.random() < 0.03,
                )
            )

    ItemPedido.objects.bulk_create(itens)
    apply_random_timestamps(itens, rng)

    # Batch query to calculate valor_total per pedido using aggregation
    pedidos_with_totals = Pedido.objects.filter(
        id__in=[p.id for p in pedidos_processados]
    ).annotate(
        total=Sum(
            F("itens__valor_total"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
    )

    # Update pedidos with calculated totals
    pedidos_to_update = []
    for pedido_with_total in pedidos_with_totals:
        pedido = next(p for p in pedidos_processados if p.id == pedido_with_total.id)
        pedido.valor_total = pedido_with_total.total or Decimal("0.00")
        pedidos_to_update.append(pedido)

    Pedido.objects.bulk_update(pedidos_to_update, ["valor_total"], batch_size=100)

    return len(itens)
