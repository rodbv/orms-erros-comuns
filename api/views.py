from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .metrics import measure_time_and_memory
from .models import Pedido
from .serializers import PedidoListSerializer


class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Hello from orms-erros-comuns!"})


class PedidoListAPIView(generics.ListAPIView):
    serializer_class = PedidoListSerializer
    pagination_class = None
    default_limit = 25

    @measure_time_and_memory
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Pedido.objects.order_by("-data_criacao").select_related("cliente")

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
