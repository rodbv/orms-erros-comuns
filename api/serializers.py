from typing import ClassVar

from rest_framework import serializers

from .models import Pedido


class PedidoListSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source="cliente.nome", read_only=True)
    cliente_sobrenome = serializers.CharField(source="cliente.sobrenome", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    valor_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields: ClassVar = [
            "id",
            "num_pedido",
            "numero_pedido",
            "cliente_nome",
            "cliente_sobrenome",
            "status",
            "status_display",
            "valor_total",
            "data_faturamento",
            "data_criacao",
        ]
