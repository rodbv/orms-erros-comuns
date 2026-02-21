from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import Cliente, ItemPedido, Pedido, Produto


class Command(BaseCommand):
    help = "Executa seeds individuais ou todos os seeds em ordem de nome de arquivo"

    def add_arguments(self, parser):
        parser.add_argument(
            "seed_file",
            nargs="?",
            help="Arquivo de seed (ex.: seeds/0010_produtos.py)",
        )
        parser.add_argument(
            "num_itens",
            nargs="?",
            type=int,
            help="Override da constante NUM_ITENS do arquivo de seed",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            default=False,
            help="Limpa dados antes de executar os seeds",
        )

    def handle(self, *args, **options):
        seed_file = options.get("seed_file")
        num_itens = options.get("num_itens")
        clear = options.get("clear", False)

        if seed_file:
            caminho_seed = self._resolver_caminho_seed(seed_file)
            if clear:
                self._limpar_dados()
            self._executar_seed(caminho_seed, num_itens)
            return

        arquivos_seed = self._listar_todos_seeds()
        if not arquivos_seed:
            self.stdout.write(self.style.WARNING("Nenhum arquivo de seed encontrado em seeds/"))
            return

        if clear:
            self._limpar_dados()

        for arquivo_seed in arquivos_seed:
            self._executar_seed(arquivo_seed, num_itens)

    def _resolver_caminho_seed(self, seed_file: str) -> Path:
        caminho = Path(seed_file)

        candidatos = []
        if caminho.is_absolute():
            candidatos.append(caminho)
        else:
            candidatos.append(Path(settings.BASE_DIR) / seed_file)
            candidatos.append(Path(settings.BASE_DIR) / "seeds" / seed_file)

        for candidato in candidatos:
            if candidato.exists() and candidato.is_file() and candidato.suffix == ".py":
                return candidato

        raise CommandError(f"Arquivo de seed não encontrado: {seed_file}")

    def _listar_todos_seeds(self) -> list[Path]:
        pasta_seeds = Path(settings.BASE_DIR) / "seeds"
        if not pasta_seeds.exists():
            return []

        arquivos = [
            arquivo
            for arquivo in pasta_seeds.glob("*.py")
            if arquivo.name != "__init__.py" and arquivo.stem[:4].isdigit()
        ]
        return sorted(arquivos, key=lambda arquivo: arquivo.name)

    def _carregar_modulo(self, caminho_seed: Path) -> ModuleType:
        nome_modulo = f"seed_{caminho_seed.stem}"
        spec = importlib.util.spec_from_file_location(nome_modulo, caminho_seed)
        if spec is None or spec.loader is None:
            raise CommandError(f"Não foi possível carregar o arquivo de seed: {caminho_seed}")

        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        return modulo

    def _executar_seed(self, caminho_seed: Path, override_num_itens: int | None) -> None:
        modulo = self._carregar_modulo(caminho_seed)

        if not hasattr(modulo, "run"):
            raise CommandError(f"Seed inválido ({caminho_seed.name}): função run ausente")

        num_itens_padrao = getattr(modulo, "NUM_ITENS", None)
        quantidade = override_num_itens if override_num_itens is not None else num_itens_padrao

        if quantidade is None:
            mensagem = (
                f"Seed inválido ({caminho_seed.name}): NUM_ITENS ausente "
                "e nenhum override informado"
            )
            raise CommandError(mensagem)

        if not isinstance(quantidade, int) or quantidade <= 0:
            raise CommandError(f"Quantidade inválida para {caminho_seed.name}: {quantidade}")

        mensagem = f"Executando {caminho_seed.name} com {quantidade} itens..."
        self.stdout.write(self.style.NOTICE(mensagem))

        resultado = modulo.run(quantidade)
        if resultado is None:
            resultado = quantidade

        self.stdout.write(self.style.SUCCESS(f"{caminho_seed.name}: {resultado} itens processados"))

    @transaction.atomic
    def _limpar_dados(self) -> None:
        self.stdout.write(self.style.WARNING("Limpando dados antes do seed (--clear)..."))
        ItemPedido.objects.all().delete()
        Pedido.objects.all().delete()
        Produto.objects.all().delete()
        Cliente.objects.all().delete()
