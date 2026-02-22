from rest_framework import serializers

from .models import ItemPedido, Pedido


class ItemPedidoPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = [
            "id",
            "quantidade",
            "valor_unitario",
            "valor_total",
        ]


class PedidoListSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source="cliente.nome", read_only=True)
    cliente_sobrenome = serializers.CharField(source="cliente.sobrenome", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    itens = ItemPedidoPreviewSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            "id",
            "num_pedido",
            "cliente_nome",
            "cliente_sobrenome",
            "status",
            "status_display",
            "valor_total",
            "data_criacao",
            "itens",
        ]
