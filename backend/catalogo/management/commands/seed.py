from datetime import datetime, time
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from catalogo.models import Categoria, Produto
from loja.models import DiasTrabalho, Loja
from solicitacao.models import ItemSolicitacao, Solicitacao, StatusSolicitacao


class Command(BaseCommand):
    help = "Popula o banco com dados reais para Loja, Categorias, Produtos e Pedidos"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Iniciando população do banco de dados..."))

        # ==========================================================
        # 1. LOJA
        # ==========================================================
        loja, criada = Loja.objects.get_or_create(
            slug="myecommerce",
            defaults={
                "nome": "MyEcommerce Store",
                "descricao": "Sua loja oficial de modas e estilo no e-commerce.",
                "telefone": "77999990000",
                "whatsapp": "77999990000",
                "email": "contato@myecommerce.com",
                "cpf": "00000000000",
                "cnpj": "",
                "cep": "45000-000",
                "rua": "Avenida Olívia Flores",
                "numero": "500",
                "referencia": "Próximo à universidade",
                "bairro": "Candeias",
                "cidade": "Vitória da Conquista",
                "estado": "BA",
                "cor_primaria": "#1E293B",
                "cor_secundaria": "#0F172A",
                "horario_funcionamento": time(8, 0),
                "horario_fechamento": time(18, 0),
                "dias_funcionamento": DiasTrabalho.SEGUNDA_A_SEXTA,
                "instagram": "https://instagram.com/myecommerce",
                "facebook": "https://facebook.com/myecommerce",
                "pix": "contato@myecommerce.com",
                "mensagem_whatsapp": "Olá! Gostaria de tirar dúvidas sobre um pedido.",
                "ativo": True,
            },
        )
        if criada:
            self.stdout.write(self.style.SUCCESS("✓ Loja criada com sucesso!"))
        else:
            self.stdout.write(self.style.SUCCESS("✓ Loja existente encontrada"))

        # ==========================================================
        # 2. CATEGORIAS
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
        for index, (nome, slug) in enumerate(categorias_data):
            categoria, _ = Categoria.objects.get_or_create(
                slug=slug,
                defaults={
                    "nome": nome,
                    "descricao": f"Produtos e itens da categoria {nome}",
                    "ativo": True,
                    "ordem": index,
                },
            )
            categorias.append(categoria)

        self.stdout.write(self.style.SUCCESS(f"✓ {len(categorias)} categorias processadas"))

        # ==========================================================
        # 3. PRODUTOS
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
        for nome, preco, estoque, cat_index in produtos_data:
            produto, _ = Produto.objects.get_or_create(
                nome=nome,
                defaults={
                    "descricao": f"{nome} confeccionado com excelente qualidade.",
                    "preco": Decimal(str(preco)),
                    "quantidade": estoque,
                    "categoria": categorias[cat_index],
                    "variacoes": ["P", "M", "G", "GG"],
                    "ativo": True,
                    "destaque": cat_index in [0, 2, 3],
                },
            )
            produtos.append(produto)

        self.stdout.write(self.style.SUCCESS(f"✓ {len(produtos)} produtos processados"))

        # ==========================================================
        # 4. SOLICITAÇÕES / PEDIDOS
        # ==========================================================
        pedidos_data = [
            {"nome": "João Silva", "telefone": "77999990001", "cidade": "Vitória da Conquista", "estado": "BA", "status": StatusSolicitacao.CONCLUIDO, "data": "2026-02-15"},
            {"nome": "Maria Santos", "telefone": "77999990002", "cidade": "Guanambi", "estado": "BA", "status": StatusSolicitacao.CONCLUIDO, "data": "2026-03-10"},
            {"nome": "Carlos Oliveira", "telefone": "77999990003", "cidade": "Brumado", "estado": "BA", "status": StatusSolicitacao.CONCLUIDO, "data": "2026-03-22"},
            {"nome": "Ana Souza", "telefone": "77999990004", "cidade": "Guanambi", "estado": "BA", "status": StatusSolicitacao.NOVO, "data": "2026-04-05"},
            {"nome": "Pedro Costa", "telefone": "77999990005", "cidade": "Caetité", "estado": "BA", "status": StatusSolicitacao.CONCLUIDO, "data": "2026-04-18"},
            {"nome": "Juliana Alves", "telefone": "77999990006", "cidade": "Vitória da Conquista", "estado": "BA", "status": StatusSolicitacao.VISTO, "data": "2026-05-03"},
            {"nome": "Lucas Pereira", "telefone": "77999990007", "cidade": "Guanambi", "estado": "BA", "status": StatusSolicitacao.CONCLUIDO, "data": "2026-05-14"},
            {"nome": "Fernanda Lima", "telefone": "77999990008", "cidade": "Brumado", "estado": "BA", "status": StatusSolicitacao.CONCLUIDO, "data": "2026-05-28"},
            {"nome": "Rafael Martins", "telefone": "77999990009", "cidade": "Caetité", "estado": "BA", "status": StatusSolicitacao.CANCELADO, "data": "2026-06-06"},
            {"nome": "Beatriz Rocha", "telefone": "77999990010", "cidade": "Guanambi", "estado": "BA", "status": StatusSolicitacao.CONCLUIDO, "data": "2026-06-15"},
            {"nome": "Gabriel Nunes", "telefone": "77999990011", "cidade": "Vitória da Conquista", "estado": "BA", "status": StatusSolicitacao.NOVO, "data": "2026-07-10"},
            {"nome": "Larissa Mendes", "telefone": "77999990012", "cidade": "Guanambi", "estado": "BA", "status": StatusSolicitacao.CONCLUIDO, "data": "2026-07-20"},
        ]

        pedidos = []
        for p_data in pedidos_data:
            pedido, _ = Solicitacao.objects.get_or_create(
                nome=p_data["nome"],
                telefone=p_data["telefone"],
                defaults={
                    "email": "",
                    "cep": "45000-000",
                    "rua": "Rua Principal",
                    "numero": "100",
                    "referencia": "Próximo à praça",
                    "bairro": "Centro",
                    "cidade": p_data["cidade"],
                    "estado": p_data["estado"],
                    "observacao": "Pedido gerado via seed.",
                    "total": Decimal("0.00"),
                    "mensagem": "Pedido de teste",
                    "status": p_data["status"],
                },
            )

            dt_aware = timezone.make_aware(datetime.strptime(p_data["data"], "%Y-%m-%d"))
            Solicitacao.objects.filter(pk=pedido.pk).update(criado_em=dt_aware, atualizado_em=dt_aware)
            pedidos.append(pedido)

        self.stdout.write(self.style.SUCCESS(f"✓ {len(pedidos)} pedidos processados"))

        # ==========================================================
        # 5. ITENS DOS PEDIDOS
        # ==========================================================
        itens_por_pedido = [
            [(0, 2), (6, 1)],
            [(1, 1), (3, 1)],
            [(2, 1), (7, 2)],
            [(4, 1)],
            [(0, 3), (8, 1)],
            [(5, 1), (9, 1)],
            [(0, 2), (1, 1), (6, 2)],
            [(3, 1), (11, 1)],
            [(7, 1)],
            [(2, 2), (8, 1)],
            [(10, 1)],
            [(14, 2), (0, 1)],
        ]

        total_itens = 0
        for pedido, itens in zip(pedidos, itens_por_pedido):
            if pedido.itens.exists():
                continue

            total_pedido = Decimal("0.00")
            for prod_index, quant in itens:
                prod = produtos[prod_index]
                subtotal = prod.preco * quant

                ItemSolicitacao.objects.create(
                    solicitacao=pedido,
                    produto=prod,
                    produto_nome=prod.nome,
                    preco_unitario=prod.preco,
                    quantidade=quant,
                    subtotal=subtotal,
                    variacao="M",
                )
                total_pedido += subtotal
                total_itens += 1

            Solicitacao.objects.filter(pk=pedido.pk).update(total=total_pedido)

        self.stdout.write(self.style.SUCCESS(f"✓ {total_itens} itens de pedido vinculados"))
        self.stdout.write(self.style.SUCCESS("=========================================="))
        self.stdout.write(self.style.SUCCESS(" BANCO DE DADOS POPULADO COM SUCESSO!"))
        self.stdout.write(self.style.SUCCESS("=========================================="))