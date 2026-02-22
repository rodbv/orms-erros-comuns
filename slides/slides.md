---
theme: default
css: ./style.css
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
transition: fade
---

# O que são ORMs?


#### Consultas feitas em código Python...

```python
queryset = Produto.objects
  .filter(preco__lte=100).order_by('-data_criacao')

if apenas_este_ano:
  queryset = queryset.filter(
    data_criacao__gte=date(2026, 1, 1)
  )
```
---


# O que são ORMs?

#### ...viram SQL em tempo de execução

```sql
SELECT "id","nome","descricao","preco"
FROM "api_produto"
WHERE ("preco" <= 100
       AND "data_criacao" >= '2026-01-01 00:00:00')
ORDER BY "data_criacao" DESC
```

---
layout: image
image: /005_25-itens.png
backgroundSize: contain
---

---

# Estrutura do nosso sistema

```mermaid
flowchart LR
  cliente[Cliente]
  pedido[Pedido]
  itens[Itens do pedido]
  produto[Produto]

  cliente -->|faz| pedido
  pedido -->|tem| itens
  produto -->|aparece em| itens
```

---

# Como funciona Django + DRF

### O fluxo: requisição HTTP → banco → JSON

```mermaid
flowchart LR
  browser[Browser pede dados]
  rotas[Rota GET /pedidos<br/>urls.py]
  view[Busca no banco<br/>views.py]
  serializer[Formata JSON<br/>serializers.py]

  browser --> rotas --> view --> serializer
  serializer -. Resposta JSON .-> browser
```

---

# Os 2 componentes essenciais

#### A view define a consulta ao banco (queryset)

```python {|3|4|0}
# views.py - Busca dados (lazy)
class PedidoListAPIView(ListAPIView):
    queryset = Pedido.objects.order_by("-data_criacao")
    serializer_class = ReportSerializer
```
<v-click>

O serializer executa a queryset e formata a resposta como JSON

```python
# serializers.py - Formata JSON
class ReportSerializer(serializers.ModelSerializer):
  cliente_nome = serializers.CharField(source="cliente.nome")
  class Meta:
    model = Pedido
    fields = ["id", "num_pedido", "cliente_nome", "status"]
```
</v-click>


---
hide: true
---

# Resultado: JSON estruturado

```json
{
  "results": [
    {
      "id": 1,
      "num_pedido": "XYZ001A",
      "cliente_nome": "João Silva",
      "status": "entregue",
      ...
    },
    {
      "id": 2,
      "num_pedido": "XYZ002B",
      ...
    }
  ],
}
```

---
layout: image
image: /005_25-itens.png
backgroundSize: contain
transition: fade
---

---
layout: image
image: /009_carregando.png
backgroundSize: contain
transition: fade
---

---
layout: image
image: /010_2000-itens.png
backgroundSize: contain
transition: fade
---

---
layout: image
image: /012_silk_4003.png
backgroundSize: contain
transition: fade
---

---
layout: image
image: /013_silk-pairs.png
backgroundSize: contain
---
---
layout: image
image: /image-8.png
backgroundSize: contain
---

---

# O problema N+1:

<Transform :scale="1.18" origin="top left">
  <ul class="mt-8 font-semibold text-left pl-10 leading-tight">
    <li>É feita <span style="color:red">uma</span> consulta para pegar todos pedidos</li>
    <li>E depois <span style="color:red">N consultas extra</span> para dados adicionais de cada pedido</li>
  </ul>
</Transform>

---
class: clientes-table-slide
---

# Vamos resolver o N+1 para clientes

#### No caso de clientes, cada pedido tem 1 cliente. Então podemos resolver trazendo os dados de clientes de cada pedido, junto com os N pedidos

| pedido.id | pedido.data_criacao | <span style="color:green">cliente.id</span> | <span style="color:green">cliente.nome</span> | <span style="color:green">cliente.sobrenome</span> |
| --------- | ------------------- | ---------- | ------------ | ----------------- |
| 9562      | 2025-01-15 10:30    | <span style="color:green">42</span>         | <span style="color:green">Maria</span>        | <span style="color:green">Silva</span>             |
| 8849      | 2025-01-14 16:45    | <span style="color:green">17</span>         | <span style="color:green">João</span>         | <span style="color:green">Santos</span>            |


---

# Fazendo um JOIN

#### No Django isso se resolve com um `select_related`

<div class="mt-8 mx-auto max-w-4xl text-left">

````md magic-move
```python{|6}
class PedidoListAPIView(generics.ListAPIView):
  serializer_class = ReportSerializer
  ...

  def get_queryset(self):
    queryset = Pedido.objects.order_by("-data_criacao")
```
```python{6-8}
class PedidoListAPIView(generics.ListAPIView):
  serializer_class = ReportSerializer
  ...

  def get_queryset(self):
    queryset = Pedido.objects
      .select_related("cliente")
      .order_by("-data_criacao")
```
````
  </div>

---
layout: image
image: /018_relatorio_sem_cliente_n1.png
backgroundSize: contain
---

---
layout: image
image: /019_2003-queries.png
backgroundSize: contain
---

---

# Vamos resolver o N+1 para itens_pedido

#### De onde ele vêm?

```json{4,7-}
{
  "results": [
    {
      "id": 12053,
      "num_pedido": "OTR450I",
      "cliente_nome": "Thiago",...
      "itens": [
          {
              "id": 30141,
              "quantidade": 3,...
          },{
              "id": 19784,
              "quantidade": 1,...
          }
      ]
    },
```

---

# prefetch_related

#### Para cada ID de pedido, vamos buscar todos os itens desses pedidos

<div class="mt-8 mx-auto max-w-4xl text-left">


````md magic-move
```python
class PedidoListAPIView(generics.ListAPIView):
    def get_queryset(self):
        queryset = Pedido.objects
          .order_by("-data_criacao")
          .select_related("cliente")
```

```python
class PedidoListAPIView(generics.ListAPIView):
    def get_queryset(self):
        queryset = Pedido.objects
          .order_by("-data_criacao")
          .select_related("cliente")
          .prefetch_related("itens")
```
````

</div>

---
layout: image
image: /022_prefetch_query.png
backgroundSize: contain
---

---
layout: image
image: /023_4-queries.png
backgroundSize: contain
---

---
layout: image
image: /024_report_2000-no-nplusone.png
backgroundSize: contain
---

---

# Tava tudo bem até uma featura nova aparecer


#### "Vamos por um campo vetorizado no modelo pra busca semântica, mas desencana que não muda nada nos reports"

<div class="mt-8 mx-auto max-w-4xl text-left">


````md magic-move
```python
class Cliente(BaseModel):
    nome = models.CharField(max_length=120)
    sobrenome = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
```
```python
class Cliente(BaseModel):
    nome = models.CharField(max_length=120)
    sobrenome = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    vectorized_data = models.TextField(blank=True, default="")
```
````

</div>


---
layout: image
image: /024_report_2000-no-nplusone.png
backgroundSize: contain
transition: fade
---

---
layout: image
image: /026_memoria.png
backgroundSize: contain
---
