from __future__ import annotations

from api.models import Cliente, ItemPedido, Pedido

NUM_ITENS = 2000
VECTOR_BYTES_TARGET = 30 * 1024  # 30 KB per item


def _build_fake_vectorized_data() -> str:
    chunk = "0.0123,-0.8877,0.3344,-0.1299,0.5555,-0.4444,0.7777,-0.2222;"
    repetitions = (VECTOR_BYTES_TARGET // len(chunk)) + 1
    payload = (chunk * repetitions)[:VECTOR_BYTES_TARGET]
    return payload


def run(num_itens: int = NUM_ITENS) -> int:
    payload = _build_fake_vectorized_data()

    clientes_qs = Cliente.objects.order_by("id")
    pedidos_qs = Pedido.objects.order_by("id")
    itens_qs = ItemPedido.objects.order_by("id")

    clientes = list(clientes_qs[:num_itens])
    pedidos = list(pedidos_qs[:num_itens])
    itens = list(itens_qs[:num_itens])

    for cliente in clientes:
        cliente.vectorized_data = payload

    for pedido in pedidos:
        pedido.vectorized_data = payload

    for item in itens:
        item.vectorized_data = payload

    if clientes:
        Cliente.objects.bulk_update(clientes, ["vectorized_data"], batch_size=500)

    if pedidos:
        Pedido.objects.bulk_update(pedidos, ["vectorized_data"], batch_size=500)

    if itens:
        ItemPedido.objects.bulk_update(itens, ["vectorized_data"], batch_size=500)

    return len(clientes) + len(pedidos) + len(itens)
