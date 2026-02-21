from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
import random

from api.models import Produto

NUM_ITENS = 100

MARCAS = {
    "Smartphone": ["Samsung", "Apple", "Motorola", "Xiaomi", "Realme"],
    "Notebook": ["Dell", "Lenovo", "Acer", "Asus", "Samsung"],
    "Monitor": ["LG", "Samsung", "AOC", "Dell", "Philips"],
    "TV": ["LG", "Samsung", "TCL", "Philips", "Sony"],
    "Fone": ["JBL", "Sony", "Philips", "Edifier", "Samsung"],
    "Mouse": ["Logitech", "Redragon", "Razer", "HyperX", "Microsoft"],
    "Teclado": ["Logitech", "Redragon", "Razer", "HyperX", "Dell"],
    "SSD": ["Kingston", "WD", "Samsung", "Crucial", "SanDisk"],
    "Roteador": ["TP-Link", "Intelbras", "D-Link", "Huawei", "Mercusys"],
    "Impressora": ["HP", "Epson", "Canon", "Brother", "Lexmark"],
}

TIPOS = [
    ("Smartphone", "Eletrônicos", Decimal("899.90"), Decimal("6999.90")),
    ("Notebook", "Informática", Decimal("2299.90"), Decimal("10999.90")),
    ("Monitor", "Informática", Decimal("599.90"), Decimal("3899.90")),
    ("TV", "Eletrônicos", Decimal("1499.90"), Decimal("12999.90")),
    ("Fone", "Eletrônicos", Decimal("79.90"), Decimal("2499.90")),
    ("Mouse", "Informática", Decimal("39.90"), Decimal("699.90")),
    ("Teclado", "Informática", Decimal("69.90"), Decimal("999.90")),
    ("SSD", "Informática", Decimal("179.90"), Decimal("1499.90")),
    ("Roteador", "Eletrônicos", Decimal("129.90"), Decimal("1599.90")),
    ("Impressora", "Informática", Decimal("499.90"), Decimal("4299.90")),
]

LINHAS = ["Essencial", "Pro", "Ultra", "Max", "Air", "Prime", "Vision", "Turbo", "Elite", "Plus"]

ESPECIFICACOES = {
    "Smartphone": ["128GB", "256GB", "5G", "Tela AMOLED", "NFC"],
    "Notebook": ["Intel i5", "Intel i7", "Ryzen 5", "16GB RAM", "SSD 512GB"],
    "Monitor": ["24\"", "27\"", "IPS", "144Hz", "QHD"],
    "TV": ["4K", "55\"", "65\"", "HDR", "Smart TV"],
    "Fone": ["Bluetooth", "Cancelamento de Ruído", "TWS", "Over-ear", "USB-C"],
    "Mouse": ["Sem fio", "6400 DPI", "RGB", "Ergonômico", "Bluetooth"],
    "Teclado": ["Mecânico", "ABNT2", "RGB", "Sem fio", "Switch Blue"],
    "SSD": ["NVMe", "SATA", "500GB", "1TB", "Leitura 3500MB/s"],
    "Roteador": ["Wi-Fi 6", "Dual Band", "Mesh", "Gigabit", "4 Antenas"],
    "Impressora": ["Multifuncional", "Tanque de Tinta", "Laser", "Wi-Fi", "Duplex"],
}


def _preco_aleatorio(minimo: Decimal, maximo: Decimal, rng: random.Random) -> Decimal:
    valor = rng.uniform(float(minimo), float(maximo))
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def run(num_itens: int = NUM_ITENS) -> int:
    rng = random.Random(20260221)

    inicio = Produto.objects.count() + 1
    produtos = []

    for indice in range(num_itens):
        tipo, categoria, preco_min, preco_max = TIPOS[indice % len(TIPOS)]
        marca = rng.choice(MARCAS[tipo])
        linha = rng.choice(LINHAS)
        especificacao = rng.choice(ESPECIFICACOES[tipo])

        nome = f"{tipo} {marca} {linha} {especificacao}"
        descricao = (
            f"{tipo} {marca} da linha {linha}, ideal para uso diário, estudos e trabalho. "
            f"Destaque para {especificacao}."
        )

        numero = inicio + indice
        sku = f"ELT-{numero:06d}"
        preco = _preco_aleatorio(preco_min, preco_max, rng)
        estoque = rng.randint(5, 180)

        produtos.append(
            Produto(
                url_foto=f"https://picsum.photos/seed/{sku}/640/480",
                nome=nome[:160],
                descricao=descricao,
                valor_unitario=preco,
                num_estoque=estoque,
                sku=sku,
                categoria=categoria,
                ativo=True,
            )
        )

    Produto.objects.bulk_create(produtos)
    return len(produtos)
