from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .metrics import measure_time_and_memory
from .models import ItemPedido, Pedido
from .serializers import ReportSerializer


class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello from orms-erros-comuns!"})


class PedidoListAPIView(generics.ListAPIView):
    serializer_class = ReportSerializer
    pagination_class = None
    default_limit = 25

    @measure_time_and_memory
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        itens_qs = ItemPedido.objects.only(
            "id",
            "pedido_id",
            "quantidade",
            "valor_unitario",
            "valor_total",
        ).order_by("id")

        queryset = (
            Pedido.objects.order_by("-data_criacao")
            .select_related("cliente")
            .prefetch_related(Prefetch("itens", queryset=itens_qs))
            .only(
                "id",
                "num_pedido",
                "status",
                "valor_total",
                "data_criacao",
                "cliente_id",
                "cliente__nome",
                "cliente__sobrenome",
            )
        )

        quantidade = self.request.query_params.get("q")
        if quantidade is None:
            return queryset[: self.default_limit]

        if str(quantidade).strip().lower() == "all":
            return queryset

        try:
            limite = int(quantidade)
        except (TypeError, ValueError):
            return queryset[: self.default_limit]

        if limite == 0:
            return queryset

        if limite <= 0:
            return queryset.none()

        return queryset[:limite]
