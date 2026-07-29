from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from catalogo.models import Categoria, Produto
from solicitacao.models import (
    Solicitacao,
    ItemSolicitacao,
    StatusSolicitacao,
)


class Command(BaseCommand):
    help = "Cria dados fictícios para testar o dashboard"

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.WARNING(
                "Criando dados de teste do dashboard..."
            )
        )

        # ==========================================================
        # 1. CATEGORIAS
        # ==========================================================

        categorias_data = [
            ("Camisetas", "camisetas"),
            ("Calças", "calcas"),
            ("Tênis", "tenis"),
            ("Vestidos", "vestidos"),
            ("Jaquetas", "jaquetas"),
            ("Acessórios", "acessorios"),
            ("Moletons", "moletons"),
            ("Bermudas", "bermudas"),
            ("Camisas", "camisas"),
            ("Promoções", "promocoes"),
        ]

        categorias = []

        for nome, slug in categorias_data:
            categoria, _ = Categoria.objects.get_or_create(
                slug=slug,
                defaults={
                    "nome": nome,
                    "descricao": f"Produtos da categoria {nome}",
                    "ativo": True,
                },
            )

            categorias.append(categoria)

        self.stdout.write(
            self.style.SUCCESS(
                f"✓ {len(categorias)} categorias criadas"
            )
        )

        # ==========================================================
        # 2. PRODUTOS
        # ==========================================================

        produtos_data = [
            ("Camiseta Básica Preta", 49.90, 30, 0),
            ("Camiseta Oversized Branca", 69.90, 25, 0),
            ("Calça Jeans Azul", 129.90, 15, 1),
            ("Tênis Casual Branco", 199.90, 12, 2),
            ("Vestido Floral", 149.90, 10, 3),
            ("Jaqueta Jeans", 179.90, 8, 4),
            ("Boné Preto", 39.90, 40, 5),
            ("Moletom Básico", 119.90, 20, 6),
            ("Bermuda Sarja", 89.90, 18, 7),
            ("Camisa Social Branca", 109.90, 14, 8),
            ("Camiseta Estampada", 59.90, 22, 0),
            ("Tênis Esportivo", 249.90, 9, 2),
            ("Vestido Preto", 139.90, 11, 3),
            ("Jaqueta Corta-Vento", 159.90, 7, 4),
            ("Moletom Oversized", 139.90, 16, 6),
        ]

        produtos = []

        for nome, preco, estoque, categoria_index in produtos_data:

            produto, _ = Produto.objects.get_or_create(
                nome=nome,
                defaults={
                    "descricao": f"{nome} para teste do dashboard.",
                    "preco": Decimal(str(preco)),
                    "quantidade": estoque,
                    "categoria": categorias[categoria_index],
                    "variacoes": ["P", "M", "G", "GG"],
                    "ativo": True,
                    "destaque": categoria_index in [0, 2, 3],
                },
            )

            produtos.append(produto)

        self.stdout.write(
            self.style.SUCCESS(
                f"✓ {len(produtos)} produtos criados"
            )
        )

        # ==========================================================
        # 3. PEDIDOS
        # ==========================================================

        pedidos_data = [
            {
                "nome": "João Silva",
                "telefone": "77999990001",
                "cidade": "Vitória da Conquista",
                "estado": "BA",
                "status": StatusSolicitacao.CONCLUIDO,
                "data": "2026-02-15",
            },
            {
                "nome": "Maria Santos",
                "telefone": "77999990002",
                "cidade": "Guanambi",
                "estado": "BA",
                "status": StatusSolicitacao.CONCLUIDO,
                "data": "2026-03-10",
            },
            {
                "nome": "Carlos Oliveira",
                "telefone": "77999990003",
                "cidade": "Brumado",
                "estado": "BA",
                "status": StatusSolicitacao.CONCLUIDO,
                "data": "2026-03-22",
            },
            {
                "nome": "Ana Souza",
                "telefone": "77999990004",
                "cidade": "Guanambi",
                "estado": "BA",
                "status": StatusSolicitacao.NOVO,
                "data": "2026-04-05",
            },
            {
                "nome": "Pedro Costa",
                "telefone": "77999990005",
                "cidade": "Caetité",
                "estado": "BA",
                "status": StatusSolicitacao.CONCLUIDO,
                "data": "2026-04-18",
            },
            {
                "nome": "Juliana Alves",
                "telefone": "77999990006",
                "cidade": "Vitória da Conquista",
                "estado": "BA",
                "status": StatusSolicitacao.VISTO,
                "data": "2026-05-03",
            },
            {
                "nome": "Lucas Pereira",
                "telefone": "77999990007",
                "cidade": "Guanambi",
                "estado": "BA",
                "status": StatusSolicitacao.CONCLUIDO,
                "data": "2026-05-14",
            },
            {
                "nome": "Fernanda Lima",
                "telefone": "77999990008",
                "cidade": "Brumado",
                "estado": "BA",
                "status": StatusSolicitacao.CONCLUIDO,
                "data": "2026-05-28",
            },
            {
                "nome": "Rafael Martins",
                "telefone": "77999990009",
                "cidade": "Caetité",
                "estado": "BA",
                "status": StatusSolicitacao.CANCELADO,
                "data": "2026-06-06",
            },
            {
                "nome": "Beatriz Rocha",
                "telefone": "77999990010",
                "cidade": "Guanambi",
                "estado": "BA",
                "status": StatusSolicitacao.CONCLUIDO,
                "data": "2026-06-15",
            },
            {
                "nome": "Gabriel Nunes",
                "telefone": "77999990011",
                "cidade": "Vitória da Conquista",
                "estado": "BA",
                "status": StatusSolicitacao.NOVO,
                "data": "2026-07-10",
            },
            {
                "nome": "Larissa Mendes",
                "telefone": "77999990012",
                "cidade": "Guanambi",
                "estado": "BA",
                "status": StatusSolicitacao.CONCLUIDO,
                "data": "2026-07-20",
            },
        ]

        pedidos = []

        for pedido_data in pedidos_data:

            pedido = Solicitacao.objects.create(
                nome=pedido_data["nome"],
                telefone=pedido_data["telefone"],
                email="",
                cep="46430000",
                rua="Rua de Teste",
                numero="100",
                referencia="Próximo à praça",
                bairro="Centro",
                cidade=pedido_data["cidade"],
                estado=pedido_data["estado"],
                observacao="Pedido criado para teste do dashboard.",
                total=Decimal("0.00"),
                mensagem="Pedido de teste",
                status=pedido_data["status"],
            )

            data = timezone.make_aware(
                datetime.strptime(
                    pedido_data["data"],
                    "%Y-%m-%d"
                )
            )

            Solicitacao.objects.filter(
                pk=pedido.pk
            ).update(
                criado_em=data,
                atualizado_em=data,
            )

            pedidos.append(pedido)

        self.stdout.write(
            self.style.SUCCESS(
                f"✓ {len(pedidos)} pedidos criados"
            )
        )

        # ==========================================================
        # 4. ITENS DOS PEDIDOS
        # ==========================================================

        itens_por_pedido = [
            # Pedido 1
            [(0, 2), (6, 1)],

            # Pedido 2
            [(1, 1), (3, 1)],

            # Pedido 3
            [(2, 1), (7, 2)],

            # Pedido 4
            [(4, 1)],

            # Pedido 5
            [(0, 3), (8, 1)],

            # Pedido 6
            [(5, 1), (9, 1)],

            # Pedido 7
            [(0, 2), (1, 1), (6, 2)],

            # Pedido 8
            [(3, 1), (11, 1)],

            # Pedido 9
            [(7, 1)],

            # Pedido 10
            [(2, 2), (8, 1)],

            # Pedido 11
            [(10, 1)],

            # Pedido 12
            [(14, 2), (0, 1)],
        ]

        total_itens = 0

        for pedido, itens in zip(pedidos, itens_por_pedido):

            total_pedido = Decimal("0.00")

            for produto_index, quantidade in itens:

                produto = produtos[produto_index]

                preco = produto.preco
                subtotal = preco * quantidade

                ItemSolicitacao.objects.create(
                    solicitacao=pedido,
                    produto=produto,
                    produto_nome=produto.nome,
                    preco_unitario=preco,
                    quantidade=quantidade,
                    subtotal=subtotal,
                    variacao="M",
                )

                total_pedido += subtotal
                total_itens += 1

            Solicitacao.objects.filter(
                pk=pedido.pk
            ).update(
                total=total_pedido
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"✓ {total_itens} itens de pedido criados"
            )
        )

        # ==========================================================
        # FINAL
        # ==========================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                " Dashboard populado com sucesso!"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )