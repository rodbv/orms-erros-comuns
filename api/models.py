import secrets
import string
from decimal import Decimal

from django.db import models


class BaseModel(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cliente(BaseModel):
    nome = models.CharField(max_length=120)
    sobrenome = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    telefone_ddd = models.CharField(max_length=3)
    telefone = models.CharField(max_length=10)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    cidade = models.CharField(max_length=120)
    ativo = models.BooleanField(default=True)
    vectorized_data = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome}".strip()


class Produto(BaseModel):
    url_foto = models.URLField()
    nome = models.CharField(max_length=160)
    descricao = models.TextField()
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    num_estoque = models.PositiveSmallIntegerField()
    sku = models.CharField(max_length=40, unique=True)
    categoria = models.CharField(max_length=80)
    ativo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.nome


class Pedido(BaseModel):
    class Status(models.TextChoices):
        ABERTO = "aberto", "Aberto"
        FATURADO = "faturado", "Faturado"
        ENTREGUE = "entregue", "Entregue"
        CANCELADO = "cancelado", "Cancelado"

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="pedidos",
        db_column="cliente_id",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTO)
    num_pedido = models.CharField(max_length=7, unique=True, db_index=True, editable=False)
    numero_pedido = models.CharField(max_length=30, unique=True)
    data_faturamento = models.DateTimeField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    vectorized_data = models.TextField(blank=True, default="")

    @staticmethod
    def gerar_num_pedido() -> str:
        return (
            "".join(secrets.choice(string.ascii_uppercase) for _ in range(3))
            + "".join(secrets.choice(string.digits) for _ in range(3))
            + secrets.choice(string.ascii_uppercase)
        )

    def save(self, *args, **kwargs):
        if self._state.adding:
            tentativas_maximas = 20
            for _ in range(tentativas_maximas):
                candidato = self.gerar_num_pedido()
                if not Pedido.objects.filter(num_pedido=candidato).exists():
                    self.num_pedido = candidato
                    break
            else:
                raise ValueError("Não foi possível gerar um num_pedido único")

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.num_pedido


class ItemPedido(BaseModel):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens",
        db_column="pedido_id",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="itens_pedido",
        db_column="produto_id",
    )
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    observacoes = models.TextField(blank=True)
    vectorized_data = models.TextField(blank=True, default="")
    numero_item = models.PositiveSmallIntegerField(default=1)
    cancelado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.valor_total = Decimal(str(self.valor_unitario)) * self.quantidade
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.pedido.num_pedido} - item {self.numero_item}"
