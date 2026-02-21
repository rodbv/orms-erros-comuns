---
marp: true
theme: default
paginate: true
---

# ORMs - Erros Comuns

Como evitar armadilhas ao usar ORMs com FastAPI

---

## Agenda

1. O que são ORMs
2. N+1 Queries
3. Lazy Loading vs Eager Loading
4. Transações mal gerenciadas
5. Migrations problemáticas
6. Boas práticas

---

## O que são ORMs?

- Object-Relational Mapping
- Abstração entre código Python e banco de dados
- Exemplos: SQLAlchemy, Django ORM, Tortoise ORM

---

## N+1 Queries

O erro mais clássico:

```python
# Ruim: 1 query para users + N queries para posts
users = session.query(User).all()
for user in users:
    print(user.posts)  # query por iteração!
```

```python
# Bom: 1 query com JOIN
users = session.query(User).options(
    joinedload(User.posts)
).all()
```

---

## Lazy Loading vs Eager Loading

- **Lazy**: carrega relacionamentos sob demanda (padrão)
- **Eager**: carrega tudo de uma vez (joinedload, subqueryload)
- Em APIs, lazy loading geralmente causa problemas

---

## Transações mal gerenciadas

```python
# Ruim: transação aberta por muito tempo
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    send_email(users)  # operação lenta dentro da transação!
    return users
```

---

## Boas práticas

- Use eager loading em endpoints de API
- Mantenha transações curtas
- Monitore queries geradas (echo=True, logging)
- Teste com volume realista de dados
- Use `select_related` / `joinedload` conscientemente

---

## Obrigado!

Perguntas?
