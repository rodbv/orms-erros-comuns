from __future__ import annotations

import datetime as dt
import random

from api.models import Cliente, Pedido

NUM_ITENS = 2000

STATUS_PESOS = [
    (Pedido.Status.ABERTO, 45),
    (Pedido.Status.FATURADO, 25),
    (Pedido.Status.ENTREGUE, 25),
    (Pedido.Status.CANCELADO, 5),
]


def _escolher_status(rng: random.Random) -> str:
    escolhas = [status for status, _peso in STATUS_PESOS]
    pesos = [peso for _status, peso in STATUS_PESOS]
    return rng.choices(escolhas, weights=pesos, k=1)[0]


def run(num_itens: int = NUM_ITENS) -> int:
    rng = random.Random(20260221)
    clientes = list(Cliente.objects.all())

    if not clientes:
        raise ValueError("Seed de pedidos requer clientes cadastrados")

    pedidos = []

    for indice in range(num_itens):
        cliente = rng.choice(clientes)
        status = _escolher_status(rng)
        numero_pedido = f"PED-{indice + 1:06d}"

        data_faturamento = None
        observacoes = ""

        if status in {Pedido.Status.FATURADO, Pedido.Status.ENTREGUE}:
            data_faturamento = dt.datetime.now(tz=dt.UTC) - dt.timedelta(days=rng.randint(1, 90))
        if status == Pedido.Status.CANCELADO:
            observacoes = "Cancelado pelo cliente"

        pedido = Pedido(
            cliente=cliente,
            status=status,
            numero_pedido=numero_pedido,
            data_faturamento=data_faturamento,
            observacoes=observacoes,
        )
        pedido.save()
        pedidos.append(pedido)

    return len(pedidos)
