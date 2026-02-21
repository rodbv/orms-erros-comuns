from __future__ import annotations

import datetime as dt
import random

from api.models import Cliente

NUM_ITENS = 80

NOMES = [
    "Ana",
    "Bruno",
    "Carla",
    "Diego",
    "Eduarda",
    "Fabio",
    "Gabriela",
    "Henrique",
    "Isabela",
    "Joao",
    "Larissa",
    "Marcos",
    "Natalia",
    "Otavio",
    "Patricia",
    "Rafael",
    "Sabrina",
    "Thiago",
    "Vitoria",
    "Yasmin",
]

SOBRENOMES = [
    "Silva",
    "Souza",
    "Oliveira",
    "Santos",
    "Lima",
    "Ferreira",
    "Pereira",
    "Gomes",
    "Almeida",
    "Ribeiro",
    "Costa",
    "Carvalho",
    "Araujo",
    "Martins",
    "Rocha",
    "Barbosa",
]

CIDADES = [
    "Sao Paulo",
    "Rio de Janeiro",
    "Belo Horizonte",
    "Curitiba",
    "Porto Alegre",
    "Salvador",
    "Fortaleza",
    "Recife",
    "Brasilia",
    "Goiania",
]

DDD = ["11", "21", "31", "41", "51", "61", "71", "81", "91"]

PROVEDORES = [
    "gmail.com",
    "outlook.com",
    "hotmail.com",
    "yahoo.com",
    "uol.com.br",
    "bol.com.br",
]


def _formatar_cpf(numero: int) -> str:
    cpf = f"{numero:011d}"
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def _gerar_email(nome: str, sobrenome: str, indice: int, dominio: str) -> str:
    return f"{nome}.{sobrenome}{indice}@{dominio}".lower()


def run(num_itens: int = NUM_ITENS) -> int:
    rng = random.Random(20260221)
    base_cpf = 12345000000
    clientes = []

    for indice in range(num_itens):
        nome = rng.choice(NOMES)
        sobrenome = rng.choice(SOBRENOMES)
        cidade = rng.choice(CIDADES)
        ddd = rng.choice(DDD)
        telefone = f"9{rng.randint(100000000, 999999999)}"

        if indice == 0:
            dominio = "bol.com.br"
        else:
            dominio = rng.choice([p for p in PROVEDORES if p != "bol.com.br"])

        email = _gerar_email(nome, sobrenome, indice + 1, dominio)
        cpf = _formatar_cpf(base_cpf + indice)
        data_nascimento = dt.date(1955, 1, 1) + dt.timedelta(days=rng.randint(0, 18000))

        clientes.append(
            Cliente(
                nome=nome,
                sobrenome=sobrenome,
                email=email,
                telefone_ddd=ddd,
                telefone=telefone,
                data_nascimento=data_nascimento,
                cpf=cpf,
                cidade=cidade,
                ativo=True,
            )
        )

    Cliente.objects.bulk_create(clientes)
    return len(clientes)
