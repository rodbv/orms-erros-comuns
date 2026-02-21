from django.apps import apps
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured

from api.models import Cliente, ItemPedido, Pedido, Produto


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "sobrenome", "email", "cidade", "ativo")
    search_fields = ("nome", "sobrenome", "email", "cpf")


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "valor_unitario", "num_estoque", "ativo")
    search_fields = ("nome", "sku", "categoria")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "num_pedido", "numero_pedido", "cliente", "status", "valor_total", "data_criacao")
    list_filter = ("status",)
    search_fields = ("num_pedido", "numero_pedido", "cliente__nome", "cliente__sobrenome")


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "produto", "quantidade", "valor_unitario", "cancelado")
    list_filter = ("cancelado",)
    search_fields = ("pedido__num_pedido", "pedido__numero_pedido", "produto__nome")


modelos_com_admin_customizado = {Cliente, Produto, Pedido, ItemPedido}

for model in apps.get_app_config("api").get_models():
    if model in modelos_com_admin_customizado:
        continue
    try:
        admin.site.register(model)
    except (admin.sites.AlreadyRegistered, ImproperlyConfigured):
        pass
