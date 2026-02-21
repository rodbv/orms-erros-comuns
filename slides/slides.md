---
theme: default
title: ORMs - Erros Comuns
info: Como evitar armadilhas ao usar ORMs com FastAPI
class: text-center
drawings:
  persist: false
transition: slide-left
mdc: true
lineNumbers: true
highlighter: shiki
themeConfig:
  primary: '#42b883'
shikiTheme:
  light: github-light
  dark: github-dark
---

# ORMs - Evitando os erros mais comuns

Como evitar armadilhas ao usar ORMs com Python

---

# O que são ORMs?

### ORM = Object-Relational Mapper: mapeia objetos Python ↔ tabelas/linhas no banco


```python
class Produto(BaseModel):
    url_foto = models.URLField()
    nome = models.CharField(max_length=160)
    descricao = models.TextField()
    valor_unitario = models.DecimalField(
      max_digits=12,
      decimal_places=2,
    )
    ...
```

---

# O que são ORMs?


#### Consultas feitas em código Python...


```python
Produto.objects.filter(
  preco__lte=100,
  data_criacao__gte=date(2026, 1, 1)
).order_by('-data_criacao')
```

<v-click>

...viram código SQL em tempo de execução, automaticamente

```sql
SELECT "id","nome","descricao","preco"
FROM "api_produto"
WHERE ("preco" <= 100
       AND "data_criacao" >= '2026-01-01 00:00:00')
ORDER BY "data_criacao" DESC
```

</v-click>

---
layout: image
image: /image-1.png
backgroundSize: contain
---

---

# Estrutura do nosso sistema

```mermaid
classDiagram
    direction LR

    class Cliente {
        id
        nome
        sobrenome
    }

    class Pedido {
        id
        cliente_id
        status
    }

    class ItemPedido {
        id
        pedido_id
        produto_id
        quantidade
    }

    class Produto {
        id
        nome
        preco
    }

    Cliente --> "faz" Pedido
    Pedido --> "contem" ItemPedido
    Produto --> "está em" ItemPedido
```

---

# Como o Django usa ORMs

### Endpoint (DRF): define a queryset lazy

**GET /api/pedidos/**

Associado à URL em `urls.py`:

```python
# api/urls.py
urlpatterns = [
    path("pedidos/", PedidoListAPIView.as_view()),
]
```

A view define a queryset:

```python
# api/views.py
class PedidoListAPIView(ListAPIView):
    queryset = Pedido.objects.order_by("-data_criacao")
    serializer_class = PedidoListSerializer
```


---

# Como o Django usa ORMs

### Serializer: transforma os dados em JSON

```python
class PedidoListSerializer(serializers.ModelSerializer):
  cliente_nome = serializers.CharField(source="cliente.nome")
  cliente_sobrenome = serializers.CharField(source="cliente.sobrenome")
  ...

  class Meta:
      model = Pedido
      fields: ClassVar = [
          "id",
          "num_pedido",
          ...
      ]
```

---

# Como o Django usa ORMs

### O resultado: JSON retornado pela API

```json
{
  "results": [
    {
      "id": 1,
      "num_pedido": "PED-001",
      "cliente_nome": "João",
      "cliente_sobrenome": "Silva",
      "status": "entregue"
    },
    {
      "id": 2,
      "num_pedido": "PED-002",
      "cliente_nome": "Maria",
      "cliente_sobrenome": "Santos",
      "status": "aberto"
    }
  ]
}
```
```
