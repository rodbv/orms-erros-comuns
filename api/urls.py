from django.urls import path

from api.views import HelloView, PedidoListAPIView

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("pedidos/", PedidoListAPIView.as_view(), name="pedido-list"),
]
