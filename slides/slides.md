---
theme: seriph
layout: cover
css: ./style.css
title: ORMs - Erros Comuns
info: Como evitar armadilhas ao usar ORMs com FastAPI
drawings:
  persist: false
transition: slide-left
mdc: true
lineNumbers: true
highlighter: shiki
background: '#002156'
class: text-center
---

# ORMs - Evitando os erros mais comuns

### Como evitar armadilhas ao usar ORMs com Python

<img src="/logo.png" alt="Python Floripa" class="cover-logo" />
<p class="cover-logo-caption">Python Floripa 93 - UniSENAI</p>

---

# O que são ORMs?

## ORM = Object-Relational Mapper{.my-8}

### Mapeia objetos Python ↔ tabelas/linhas no banco{.my-8}


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
class: estrutura-slide
---

# Estrutura do nosso sistema

<div class="mx-auto w-[82%] mt-16">

```mermaid
%%{init: {"theme": "base", "themeVariables": {"background": "transparent", "fontSize": "24px", "lineColor": "#feb811", "primaryColor": "#033388", "primaryBorderColor": "#feb811", "primaryTextColor": "#f8fbff", "secondaryColor": "#033388", "secondaryTextColor": "#f8fbff", "tertiaryColor": "#033388", "tertiaryBorderColor": "#feb811", "tertiaryTextColor": "#f8fbff", "edgeLabelBackground": "#033388"}}}%%
flowchart LR
  cliente[Cliente]
  pedido[Pedido]
  item[ItemPedido]
  produto[Produto]

  cliente -->|faz| pedido
  pedido -->|contém| item
  produto -->|aparece em| item

  classDef entidade fill:#033388,stroke:#feb811,stroke-width:2px,color:#f8fbff;
  class cliente,pedido,item,produto entidade;
```

</div>

---

# Como funciona Django + DRF

#### A `urls.py` roteia para a view

```python
# urls.py
urlpatterns = [
  path("pedidos/", PedidoListAPIView.as_view()),
]
```
<v-click>

#### A view define a consulta ao banco (queryset){.my-8}

```python {|3|4}
# views.py - Busca dados (lazy)
class PedidoListAPIView(ListAPIView):
    queryset = Pedido.objects.order_by("-data_criacao")
    serializer_class = ReportSerializer
```
</v-click>

---

# Response sai: Serializer → JSON

#### O serializer executa a queryset e formata a resposta como JSON{.my-8}

```python
# serializers.py - Formata JSON
class ReportSerializer(serializers.ModelSerializer):
  cliente_nome = serializers.CharField(source="cliente.nome")
  class Meta:
    model = Pedido
    fields = ["id", "num_pedido", "cliente_nome", "status"]
```


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
image: /014_query-cliente.png
backgroundSize: contain
---

---

# O problema N+1:

<Transform :scale="1.18" origin="top left">
  <ul class="mt-8 font-semibold text-left pl-10 leading-tight">
    <li>É feita <span style="color:#feb811">uma</span> consulta para pegar todos pedidos</li>
    <li>E depois <span style="color:#feb811">N consultas extra</span> para dados adicionais de cada pedido</li>
  </ul>
</Transform>

---
class: clientes-table-slide
---

# Bora resolver o N+1 de clientes

#### No caso de clientes, cada pedido tem 1 cliente. Então podemos resolver trazendo os dados de clientes de cada pedido, junto com os N pedidos

| pedido.id | pedido.data_criacao | cliente.id | cliente.nome | cliente.sobrenome |
| --------- | ------------------- | ---------- | ------------ | ----------------- |
| 9562      | 2025-01-15 10:30    | 42         | Maria        | Silva             |
| 8849      | 2025-01-14 16:45    | 17         | João         | Santos            |


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

# N+1 em itens_pedido, na prática

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

#### Para cada ID de pedido, a ideia aqui é buscar todos os itens desses pedidos

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

<div class="speech-bubble">

Bora colocar um campo vetorizado no modelo pra busca semântica, mas desencana que não muda nada nos reports, vai dar bom!
<div class="text-sm opacity-70 text-right mt-2">— Um colega, sexta 17:45</div>
</div>

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

---
layout: image
image: /028_query-with-all-cols.png
backgroundSize: contain
---

---

# Como buscar apenas os valores que o serializer realmente usa?

````md magic-move

```python
def get_queryset(self):
    queryset = (
        Pedido.objects.order_by("-data_criacao")
        .select_related("cliente")
        .prefetch_related(Prefetch("itens")
    )
```
```python{|5-}
def get_queryset(self):
    queryset = (
        Pedido.objects.order_by("-data_criacao")
        .select_related("cliente")
        .prefetch_related(Prefetch("itens", queryset=itens_qs))
        .only(
            "id",
            "num_pedido",
            "status",
            #...
        )
    )
```
````

---
layout: image
image: /030_less_memory.png
backgroundSize: contain
---

---
layout: image
image: /031_todo-dia.png
backgroundSize: contain
---

---

# Garantindo que n+1 não volta com testes

<div class="mt-8 mx-auto max-w-4xl text-left">


```python
def test_pedidos_list_endpoint_sem_n_mais_1(django_assert_num_queries):
    self.cria_pedidos_com_itens(10)

    with django_assert_num_queries(2):
        response = self.client.get("/api/pedidos/")

    assert response.status_code == HTTPStatus.OK
```

</div>

---

# Garantindo que apenas as colunas esperadas são serializadas

```python
@pytest.mark.django_db
def test_pedidos_list_endpoint_serializa_apenas_colunas_esperadas():
    self.cria_pedidos_com_itens(10)

    response = self.client.get("/api/pedidos/")

    expected_pedido_fields = {"id", "num_pedido", ... }
    expected_item_fields = {"id", "quantidade",...}

    for pedido_payload in data["results"]:
        assert set(pedido_payload.keys()) == expected_pedido_fields

        for item_payload in pedido_payload["itens"]:
            assert set(item_payload.keys()) == expected_item_fields

```

---

# Mas e se eu uso Fast API?

<Transform :scale="1.18" origin="top left">
  <ul class="mt-8 font-semibold text-left pl-10 leading-tight">
    <li>N+1, memory leaks, e coluna não-serializada são <span style="color:#feb811">problemas universais</span> de qualquer ORM</li>
    <li>Não importa se usar FastAPI, Flask, ou outro framework</li>
    <li>Quem usa padrões de repositório também!</li>
  </ul>
</Transform>

<div class="mt-8 mx-auto max-w-4xl text-left">

| Django ORM | SQLAlchemy |
| --- | --- |
| `.select_related()` | `.joinedload()` |
| `.prefetch_related()` | `.selectinload()` ou `.contains_eager()` |
| `.only()` | `query(Model.id, Model.nome, ...)` ou `defer()` |

</div>

---
layout: section
---

# Então lembrem-se amiguinhes! 🚀

<div class="text-lg mt-16">

- N+1 queries são o erro mais comum — use `.select_related()` e `.prefetch_related()`
- Testes de regressão são fundamentais — `django_assert_num_queries()` previne surpresas
- Colunas desnecessárias consomem memória — busque só que você quer com `.only()`
- Estes problemas existem em qualquer ORM — FastAPI, Flask, SQLAlchemy, etc
- Código gerado por IA frequentemente tem esses erros — entender esses conceitos é crítico para revisar e corrigir

</div>

---
layout: end
---

# Obrigado!

- rodrigo.vieira@gmail.com
- https://linkedin.com/in/rodrigobvieira

---

# Pós-crédito: E se eu uso Pandas?

#### O mesmo tipo de erro é possível: carregar dados em loop

❌ N+1: iterrows + lookup - busca sequencial lenta
```python
for _, pedido in pedidos.iterrows():
    cliente = clientes[
        clientes['id'] == pedido['cliente_id']
    ]
```

✅ Merge vetorizado - operação vetorizada, uma passada
```python
resultado = pedidos.merge(
    clientes[['id', 'nome']],
    left_on='cliente_id',
    right_on='id'
)
```

---
layout: end
---

# Agora tchau mesmo

- rodrigo.vieira@gmail.com
- https://linkedin.com/in/rodrigobvieira
