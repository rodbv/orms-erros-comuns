import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_hello_endpoint():
    client = APIClient()
    response = client.get("/api/hello/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from orms-erros-comuns!"}


@pytest.mark.django_db
def test_pedidos_list_endpoint():
    pedido_1 = baker.make(
        "api.Pedido",
        numero_pedido="PED-2001",
        status="aberto",
    )
    pedido_2 = baker.make(
        "api.Pedido",
        numero_pedido="PED-2002",
        status="faturado",
    )

    baker.make(
        "api.ItemPedido",
        pedido=pedido_1,
        quantidade=2,
        valor_unitario="10.50",
    )
    baker.make(
        "api.ItemPedido",
        pedido=pedido_2,
        quantidade=1,
        valor_unitario="99.90",
    )

    client = APIClient()
    response = client.get("/api/pedidos/")

    assert response.status_code == 200
    data = response.json()
    assert "elapsed" in data
    assert "memory_mb" in data
    assert len(data["results"]) == 2
    assert {item["id"] for item in data["results"]} == {pedido_1.id, pedido_2.id}

    primeiro = data["results"][0]
    assert {
        "id",
        "num_pedido",
        "cliente_nome",
        "cliente_sobrenome",
        "status",
        "status_display",
        "valor_total",
        "data_criacao",
        "itens",
    }.issubset(primeiro.keys())
    assert "vectorized_data" not in primeiro

    primeiro_item = primeiro["itens"][0]
    assert {"id", "quantidade", "valor_unitario", "valor_total"} == set(primeiro_item.keys())


@pytest.mark.django_db
def test_pedidos_list_endpoint_respeita_q():
    pedidos = baker.make(
        "api.Pedido",
        numero_pedido=baker.seq("PED-"),
        _quantity=3,
    )

    for pedido in pedidos:
        baker.make(
            "api.ItemPedido",
            pedido=pedido,
            quantidade=1,
            valor_unitario="10.00",
        )

    client = APIClient()
    response = client.get("/api/pedidos/?q=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2
    assert "elapsed" in data
    assert "memory_mb" in data


@pytest.mark.django_db
def test_pedidos_list_endpoint_q_zero_retorna_tudo():
    baker.make(
        "api.Pedido",
        numero_pedido=baker.seq("PED-"),
        _quantity=30,
    )

    client = APIClient()
    response_sem_q = client.get("/api/pedidos/")
    response_com_q_zero = client.get("/api/pedidos/?q=0")

    assert response_sem_q.status_code == 200
    assert response_com_q_zero.status_code == 200
    assert len(response_sem_q.json()["results"]) == 25
    assert len(response_com_q_zero.json()["results"]) == 30


@pytest.mark.django_db
def test_pedidos_list_endpoint_q_all_retorna_tudo():
    baker.make(
        "api.Pedido",
        numero_pedido=baker.seq("PED-"),
        _quantity=30,
    )

    client = APIClient()
    response = client.get("/api/pedidos/?q=all")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 30


@pytest.mark.django_db
def test_pedidos_list_endpoint_sem_n_plus_one(django_assert_num_queries):
    pedidos = baker.make(
        "api.Pedido",
        numero_pedido=baker.seq("PED-"),
        _quantity=8,
    )

    for pedido in pedidos:
        baker.make(
            "api.ItemPedido",
            pedido=pedido,
            quantidade=2,
            valor_unitario="12.34",
        )

    client = APIClient()

    with django_assert_num_queries(2):
        response = client.get("/api/pedidos/?q=all")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 8


@pytest.mark.django_db
def test_pedidos_list_endpoint_serializa_apenas_colunas_esperadas():
    pedidos = baker.make(
        "api.Pedido",
        numero_pedido=baker.seq("PED-"),
        _quantity=2,
    )

    for pedido in pedidos:
        baker.make(
            "api.ItemPedido",
            pedido=pedido,
            quantidade=1,
            valor_unitario="15.00",
        )

    client = APIClient()
    response = client.get("/api/pedidos/?q=all")

    assert response.status_code == 200
    data = response.json()

    expected_pedido_fields = {
        "id",
        "num_pedido",
        "cliente_nome",
        "cliente_sobrenome",
        "status",
        "status_display",
        "valor_total",
        "data_criacao",
        "itens",
    }
    expected_item_fields = {"id", "quantidade", "valor_unitario", "valor_total"}

    for pedido_payload in data["results"]:
        assert set(pedido_payload.keys()) == expected_pedido_fields
        assert "vectorized_data" not in pedido_payload

        for item_payload in pedido_payload["itens"]:
            assert set(item_payload.keys()) == expected_item_fields
            assert "vectorized_data" not in item_payload
