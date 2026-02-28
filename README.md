
# ORMs - Erros Comuns

> **Nota:** Este branch (`ddt`) possui suporte ao Django Debug Toolbar. Para rodar o projeto com o Debug Toolbar ativado, use o comando:
>
>     just ddt
>
O Debug Toolbar estará disponível em http://localhost:8000/__debug__/

Repositório da talk educacional **"ORMs em Python: evitando os erros mais comuns"** apresentada na **Python Floripa 93** em 28/02/2026.

Armadilhas comuns ao usar ORMs, com foco em Django/DRF mas cobrindo conceitos universais (FastAPI/SQLAlchemy, Pandas).

**Duração da Talk**: ~35-40 minutos + Q&A

## 🎯 O que você vai aprender

- **N+1 Queries**: Como detectar e resolver com `select_related()` e `prefetch_related()`
- **Vazamentos de Memória**: Evitar carregar colunas desnecessárias com `.only()` e `.defer()`
- **Testes de Regressão de Query**: Proteger otimizações com `django_assert_num_queries()`
- **Conceitos Universais**: Mesmo problema em FastAPI/SQLAlchemy e Pandas

## 🚀 Stack

**Backend**: Python 3.14 + Django 6.0.2 + Django REST Framework
**Frontend**: React + Vite
**Slides**: Slidev (tema Dracula)
**Banco de dados**: SQLite3

## 📦 Configuração

### Pré-requisitos
- Python 3.14+
- Node.js 18+
- `uv` (gerenciador de pacotes Python)
- `just` (executor de tarefas)

### Backend (Django + DRF)

```bash
# Instalar dependências
uv sync

# Aplicar migrações
just m migrate

# Popular banco com dados de exemplo
just reseed

# Rodar servidor
just run
```

**Endpoints**:
- API: http://localhost:8000/api/pedidos/
- Admin: http://localhost:8000/admin/

### Frontend (React)

```bash
cd frontend && npm install
npm run dev
# Abre em http://localhost:3000
```

### Testes

```bash
# Rodar bateria completa
just test

# Rodar com modo verbose
just test -v

# Arquivo: tests/test_api.py
# - test_pedidos_list_endpoint_sem_n_mais_1: Valida que não há N+1
# - test_pedidos_list_endpoint_serializa_apenas_colunas_esperadas: Valida colunas esperadas
```

## 🎤 Slides (Slidev)

**Live Slides**: https://rodbv.github.io/orms-erros-comuns/

```bash
# Instalar dependências
just slides-install

# Modo desenvolvimento (live reload)
just slides

# Build para produção
just slides-build
```

**Estrutura de Slides**:
1. Intro: O que são ORMs
2. Fundamentos de Django + DRF
3. Problema N+1 + diagnóstico
4. Solução select_related()
5. Solução prefetch_related()
6. Otimização de memória com .only()
7. Testes de regressão de query
8. Equivalentes FastAPI/SQLAlchemy
9. Equivalente N+1 em Pandas (apêndice)
10. Aprendizados principais
11. Obrigado!

## 📊 Projeto Demo

O repositório contém um sistema de **Pedidos + Clientes + Itens** que reproduz o problema N+1:

```
Cliente (1) → (N) Pedido → (N) ItemPedido
```

**Dados**: ~2500 clientes, ~2500 pedidos com itens

## 🔧 Utilitários

```bash
just run          # Servidor dev Django
just test         # Pytest
just m migrate    # Django migrations
just reseed       # Popular banco
just vacuum       # SQLite VACUUM
just shell        # Django shell_plus (IPython)
just slides       # Slidev (desenvolvimento)
```

## 🎓 Conceitos Chave

### Otimização do Django ORM

| Problema | Solução |
|----------|---------|
| N+1 ForeignKey | `.select_related("campo")` |
| N+1 Reverse/M2M | `.prefetch_related("campo")` |
| Colunas extras | `.only("id", "nome", ...)` |
| Regressão de Query | `django_assert_num_queries(N)` |

### Equivalentes em Outras ORMs

- **FastAPI + SQLAlchemy**: `.joinedload()`, `.selectinload()`, `query(Model.id, Model.nome)`
- **Pandas**: `.merge()` vs `iterrows()` + lookup

## 📁 Estrutura do Projeto

```
.
├── api/                    # Django app principal
│   ├── models.py          # Cliente, Pedido, ItemPedido
│   ├── views.py           # PedidoListAPIView (otimizado)
│   ├── serializers.py     # ReportSerializer
│   └── migrations/
├── backend/               # Configurações Django
├── frontend/              # React (Vite)
├── slides/                # Apresentação Slidev
│   ├── slides.md
│   ├── style.css
│   └── public/            # Capturas de tela
├── seeds/                 # Dados de exemplo
├── tests/                 # Bateria de testes
├── db.sqlite3            # Banco de dados
└── justfile              # Definições de tarefas

```

## 📝 Licença

**Código**: MIT License - veja [LICENSE](LICENSE)

**Slides**: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
- Você pode usar, modificar e compartilhar os slides desde que atribua autoria e mantenha a mesma licença

## 👤 Autor

Rodrigo Vieira
📧 rodrigo.vieira@gmail.com

---

**Última atualização**: Fevereiro 2026
